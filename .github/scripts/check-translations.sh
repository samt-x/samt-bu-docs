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
#
# Hastighet: én git log per repo, og all sammenligning i ett awk-program. Den første utgaven kjørte
# flere git- og grep-kall per side, og brukte over 5 minutter i Git Bash på Windows (s110).

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
SINCE=$(date -d "$BASELINE" +%s)

# Leser fire seksjoner fra stdin: unntakene, oversettelses-commitene, git log med filnavn
# (nyeste først) og filene i content/. Skriver én linje per treff:
#   gruppe <tab> sti <tab> grunn <tab> commit å vise diff fra <tab> sti å vise diff for
# Bare POSIX-awk (mawk på GitHub, gawk i Git Bash).
AWK='
/^@@SECTION / { sec = $2; next }

sec == "IGN" {
  if ($0 ~ /^[ \t]*(#|$)/) next
  ni++; ik[ni] = $1; ih[ni] = $2; next
}

sec == "TR" { if ($0 != "") tr[$0] = 1; next }

sec == "LOG" {
  if ($0 == "") next
  if (substr($0, 1, 4) == "@@C ") {
    gi++; ch = $2; ct = $3; cs = $4
    cbot = (index($0, "[bot]") > 0); ctr = (ch in tr)
    next
  }
  f = $0; k = ++n[f]
  G[f, k] = gi; B[f, k] = cbot; T[f, k] = ctr; CT[f, k] = ct
  if (k == 1) lastdate[f] = cs
  if (!cbot && !(f in lh)) { lh[f] = ch; lhg[f] = gi }
  next
}

sec == "FILES" { nf++; F[nf] = substr($0, length(dir) + 2); exists[F[nf]] = 1; next }

# Menneskelige endringer på f nyere enn commit nr. fromg, oversettelser ikke medregnet
function edits_after(f, fromg, since,   k, c) {
  c = 0
  for (k = 1; k <= n[f]; k++) {
    if (G[f, k] >= fromg) break
    if (!B[f, k] && !T[f, k] && (since == 0 || CT[f, k] >= since)) c++
  }
  return c
}

function ignored(key, h,   i) {
  for (i = 1; i <= ni; i++) {
    if (ih[i] == "*" && index(key, ik[i]) == 1) return 1
    if (ik[i] == key && h != "" && index(h, ih[i]) == 1) return 1
  }
  return 0
}

# Brødteksten (etter andre ---): tegn, overskrifter, plassholder alene på en linje
function stats(path,   line, l, m) {
  m = 0; S_c = 0; S_h = 0; S_pe = 0; S_pn = 0
  while ((getline line < path) > 0) {
    if (m >= 2) {
      S_c += length(line) + 1
      if (match(line, /^#+ /) && RLENGTH <= 7) S_h++
      l = tolower(line)
      if (l ~ /^[[:space:]*_>]*(english translation tbd|todo:? english translation)[^a-z]*$/) S_pe = 1
      if (l ~ /^[[:space:]*_>]*norsk oversettelse tbd[^a-z]*$/) S_pn = 1
    }
    if (line ~ /^---[[:space:]]*$/) m++
  }
  close(path)
}

function out(g, p, r, h, dp) { print g "\t" p "\t" r "\t" h "\t" dp }

END {
  for (i = 1; i <= nf; i++) {
    rel = F[i]
    if (rel ~ /\.en\.md$/) {
      nbr = substr(rel, 1, length(rel) - 6) ".nb.md"
      if (!(nbr in exists) && !ignored(repo "/" rel, "")) out("nb", rel, "norsk mangler", "", "")
      continue
    }
    enr = substr(rel, 1, length(rel) - 6) ".en.md"; key = repo "/" rel
    if (!(enr in exists)) { if (!ignored(key, "")) out("en", rel, "engelsk mangler", "", ""); continue }

    # Siste menneskelige commit på en av de to filene, for unntakene
    last = ""
    if (rel in lh) last = lh[rel]
    if ((enr in lh) && (last == "" || lhg[enr] < lhg[rel])) last = lh[enr]
    if (ignored(key, last)) continue

    stats(dir "/" enr); ec = S_c; eh = S_h
    if (S_pe) { out("en", enr, "plassholder", "", ""); continue }
    stats(dir "/" rel); nc = S_c; nh = S_h
    if (S_pn) { out("nb", rel, "plassholder", "", ""); continue }

    if ((enr in lh) && edits_after(rel, lhg[enr], 0) > 0) {
      out("en", rel, "norsk endret " lastdate[rel], lh[enr], rel); continue
    }
    if ((rel in lh) && edits_after(enr, lhg[rel], since) > 0) {
      out("nb", enr, "engelsk endret " lastdate[enr], lh[rel], enr); continue
    }
    if (nh != eh || (nc > 300 && ec * 100 < nc * 60) || (ec > 300 && nc * 100 < ec * 60))
      out("st", rel, "overskrifter nb " nh " / en " eh ", tegn nb " nc " / en " ec, "", "")
  }
}'

scan() {
  local dir="$1" repo="$2"
  {
    echo "@@SECTION IGN"
    [ -f "$IGNORE" ] && cat "$IGNORE"
    echo "@@SECTION TR"
    git -C "$dir" log --no-merges --grep='^Oversatt-fra:' --format=%H -- content
    echo "@@SECTION LOG"
    git -C "$dir" -c core.quotepath=false log --no-merges --format='@@C %H %ct %cs %ae|%aN' --name-only -- content
    echo "@@SECTION FILES"
    find "$dir/content" \( -name '*.nb.md' -o -name '*.en.md' \) | LC_ALL=C sort
  } | awk -v repo="$repo" -v dir="$dir" -v since="$SINCE" "$AWK"
}

# Endringene på kildesiden siden oversettelsen, uten frontmatter-støy
show_diff() {
  git -C "$1" diff --no-color "$2..HEAD" -- "$3" | grep -E '^[-+]' \
    | grep -vE '^(\+\+\+|---)|^[-+](lastmod|last_editor|weight|id):' | sed 's/^/      /'
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
  while IFS=$'\t' read -r group path reason from diffpath; do
    details=""
    if [ "$DIFF" = 1 ] && [ -n "$from" ]; then
      details="$(show_diff "$dir" "$from" "$diffpath")"$'\n'
    fi
    add "$group" "$repo" "$path" "$reason" "$details"
  done < <(scan "$dir" "$repo")
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
