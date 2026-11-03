#!/usr/bin/env bash
# Finner sider der norsk og engelsk ikke er i takt, i begge retninger, i alle innholdsrepoene
# under --root (mapper med .git og content/). Endrer ingenting.
#
#   bash check-translations.sh --root <mappe>              # oversikt
#   bash check-translations.sh --root <mappe> --diff       # + endringene som må oversettes
#   bash check-translations.sh --root <mappe> --repo <r>   # bare ett repo
#   bash check-translations.sh --root <mappe> --markdown   # issue-tekst (workflowen translations.yml)
#
# Lokalt kjøres den via S:/app-data/github/samt-x-repos/check-translations.sh, som setter --root.
#
# Grupper:
#   TIL ENGELSK  engelsk mangler, har plassholder («English translation TBD»), eller norsk er endret
#                etter siste commit på engelsk
#   TIL NORSK    det samme motsatt vei (plassholder «Norsk oversettelse TBD»)
#   STRUKTUR     ulikt antall overskrifter, eller den ene brødteksten under 60 % av den andre.
#                Fanger det tidssjekken ikke ser: en commit som rørte begge filene (lenkeretting,
#                omdøping) uten at den andre ble oversatt.
#
# Commits som ikke telles som endring:
#   - bot-commits («Auto: oppdater lastmod», uuid-commitene), som rører begge filene
#   - oversettelser, merket med linjen «Oversatt-fra: nb» eller «Oversatt-fra: en» i commit-meldingen.
#     Uten merket ville selve oversettelsen få kildesiden til å se utdatert ut.
# Engelsk → norsk sjekkes bare for commits fra BASELINE (2026-11-03 kl. 12). Før det var norsk alltid
# master, og oversettelsene i s110 er ikke merket.
#
# Unntak står i ../translation-ignore.txt.

# Med klokkeslett og sone: bare dato gir dagens klokkeslett i git. Etter siste oversettelse i s110 (01:42).
BASELINE="2026-11-03 12:00 +0100"
ROOT=""; DIFF=0; ONLY=""; MD=0
IGNORE="$(cd "$(dirname "$0")/.." && pwd)/translation-ignore.txt"
while [ $# -gt 0 ]; do
  case "$1" in
    --root) ROOT="$2"; shift ;;
    --diff) DIFF=1 ;;
    --repo) ONLY="$2"; shift ;;
    --markdown) MD=1 ;;
  esac
  shift
done
[ -d "$ROOT" ] || { echo "Bruk: check-translations.sh --root <mappe med repoene>" >&2; exit 2; }
ROOT="$(cd "$ROOT" && pwd)"

# Plassholderen står alene på en linje (temaet skriver «*English translation TBD.*»). Sider som
# omtaler plassholderen i en setning, skal ikke treffes.
PLACEHOLDER_EN='^[[:space:]*_>]*(english translation TBD|TODO:? english translation)[^a-z]*$'
PLACEHOLDER_NB='^[[:space:]*_>]*norsk oversettelse TBD[^a-z]*$'

humans() { grep -v '\[bot\]'; }

# Siste menneskelige commit på stiene (også oversettelser)
last_human() {
  local dir="$1"; shift
  git -C "$dir" log --format='%H|%ae|%aN' -- "$@" 2>/dev/null | humans | head -1 | cut -d'|' -f1
}

# Menneskelige endringer på en sti etter en commit, oversettelser ikke medregnet. Valgfri dato.
edits_after() {
  local dir="$1" from="$2" path="$3" since="$4"
  git -C "$dir" log --invert-grep --grep='^Oversatt-fra:' ${since:+--since="$since"} \
    --format='%ae|%aN' "$from..HEAD" -- "$path" | humans | wc -l
}

# Endringene på kildesiden siden oversettelsen, uten frontmatter-støy
show_diff() {
  git -C "$1" diff --no-color "$2..HEAD" -- "$3" | grep -E '^[-+]' \
    | grep -vE '^(\+\+\+|---)|^[-+](lastmod|last_editor|weight|id):' | sed 's/^/      /'
}

# Brødteksten uten frontmatter
body() { awk 'n >= 2; /^---[[:space:]]*$/ { n++ }' "$1"; }

# Unntak: «<repo>/<sti> <commit>» gjelder til en av filene får en ny menneskelig commit.
# «<repo>/<mappe>/ *» gjelder alt under mappa.
ignored() {
  [ -f "$IGNORE" ] || return 1
  awk -v k="$1" -v h="$2" '
    /^[[:space:]]*(#|$)/ { next }
    ($2 == "*" && index(k, $1) == 1) || ($1 == k && h != "" && index(h, $2) == 1) { f = 1 }
    END { exit !f }' "$IGNORE"
}

to_en=""; to_nb=""; struct=""
n_en=0; n_nb=0; n_struct=0

# add <gruppe> <repo> <sti> <grunn> [<detaljer>]
add() {
  local line
  if [ "$MD" = 1 ]; then
    line="- [$2/$3](https://github.com/SAMT-X/$2/blob/main/${3// /%20}) – $4"$'\n'
  else
    line="  $2/$3  ($4)"$'\n'"$5"
  fi
  case "$1" in
    en) to_en+="$line"; n_en=$((n_en + 1)) ;;
    nb) to_nb+="$line"; n_nb=$((n_nb + 1)) ;;
    st) struct+="$line"; n_struct=$((n_struct + 1)) ;;
  esac
}

for d in "$ROOT"/*/; do
  repo="$(basename "$d")"
  [ -e "$d.git" ] && [ -d "${d}content" ] || continue
  [ -n "$ONLY" ] && [ "$repo" != "$ONLY" ] && continue
  dir="${d%/}"

  # Engelske sider uten norsk
  while IFS= read -r en; do
    rel="${en#$dir/}"
    [ -f "$dir/${rel%.en.md}.nb.md" ] && continue
    ignored "$repo/$rel" "" || add nb "$repo" "$rel" "norsk mangler"
  done < <(find "$dir/content" -name '*.en.md' | sort)

  while IFS= read -r nb; do
    rel="${nb#$dir/}"
    en_rel="${rel%.nb.md}.en.md"
    en="$dir/$en_rel"
    key="$repo/$rel"
    if [ ! -f "$en" ]; then
      ignored "$key" "" || add en "$repo" "$rel" "engelsk mangler"
      continue
    fi
    last=$(last_human "$dir" "$rel" "$en_rel")
    ignored "$key" "$last" && continue

    if grep -qiE "$PLACEHOLDER_EN" "$en"; then
      add en "$repo" "$en_rel" "plassholder"
      continue
    fi
    if grep -qiE "$PLACEHOLDER_NB" "$nb"; then
      add nb "$repo" "$rel" "plassholder"
      continue
    fi

    nb_commit=$(last_human "$dir" "$rel")
    en_commit=$(last_human "$dir" "$en_rel")
    if [ -n "$en_commit" ] && [ "$(edits_after "$dir" "$en_commit" "$rel")" -gt 0 ]; then
      add en "$repo" "$rel" "norsk endret $(git -C "$dir" log -1 --format=%cs -- "$rel")" \
        "$([ "$DIFF" = 1 ] && show_diff "$dir" "$en_commit" "$rel" && echo)"
      continue
    fi
    if [ -n "$nb_commit" ] && [ "$(edits_after "$dir" "$nb_commit" "$en_rel" "$BASELINE")" -gt 0 ]; then
      add nb "$repo" "$en_rel" "engelsk endret $(git -C "$dir" log -1 --format=%cs -- "$en_rel")" \
        "$([ "$DIFF" = 1 ] && show_diff "$dir" "$nb_commit" "$en_rel" && echo)"
      continue
    fi

    # Struktur: ulikt antall overskrifter, eller den ene under 60 % av den andre
    nb_h=$(body "$nb" | grep -cE '^#{1,6} ')
    en_h=$(body "$en" | grep -cE '^#{1,6} ')
    nb_c=$(body "$nb" | wc -c)
    en_c=$(body "$en" | wc -c)
    if [ "$nb_h" != "$en_h" ] \
      || { [ "$nb_c" -gt 300 ] && [ $((en_c * 100)) -lt $((nb_c * 60)) ]; } \
      || { [ "$en_c" -gt 300 ] && [ $((nb_c * 100)) -lt $((en_c * 60)) ]; }; then
      add st "$repo" "$rel" "overskrifter nb $nb_h / en $en_h, tegn nb $nb_c / en $en_c"
    fi
  done < <(find "$dir/content" -name '*.nb.md' | sort)
done

if [ "$MD" = 1 ]; then
  echo "<!-- Generert av samt-bu-docs/.github/scripts/check-translations.sh (workflowen translations.yml). Ikke rediger, teksten overskrives. -->"
  if [ $((n_en + n_nb + n_struct)) = 0 ]; then
    echo "Alle sidene er i takt på norsk og engelsk."
  else
    echo "Sider der norsk og engelsk ikke er i takt. Lista oppdateres ved hver endring i innholdsrepoene."
  fi
  echo
  echo "Oversettelsen gjøres inntil videre av Claude Code i Eriks sesjoner, se [Oversettelse](https://docs.samt-bu.no/prosjektleveranser/loesninger/samhandlingsplattform/samt-bu-docs/teknisk-dokumentasjon/oversettelse/)."
  [ "$n_en" -gt 0 ] && printf "\n### Til engelsk (%s)\n\n%s" "$n_en" "$to_en"
  [ "$n_nb" -gt 0 ] && printf "\n### Til norsk (%s)\n\n%s" "$n_nb" "$to_nb"
  [ "$n_struct" -gt 0 ] && printf "\n### Sjekk strukturen (%s)\n\nUlikt antall overskrifter eller svært ulik lengde. Kan være en ufullstendig oversettelse.\n\n%s" "$n_struct" "$struct"
  exit 0
fi

echo "== TIL ENGELSK ($n_en)"
printf "%s" "$to_en"
echo ""
echo "== TIL NORSK ($n_nb)"
printf "%s" "$to_nb"
echo ""
echo "== STRUKTUR: ulikt antall overskrifter, eller den ene under 60 % av den andre ($n_struct)"
printf "%s" "$struct"
echo ""
echo "Sum: $n_en til engelsk, $n_nb til norsk, $n_struct struktur."
