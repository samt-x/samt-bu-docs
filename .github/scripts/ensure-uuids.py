#!/usr/bin/env python3
"""ensure-uuids.py

Sikrer at alle _index.nb.md / _index.en.md-par i content/
har ett felles UUID i frontmatter-feltet 'id'.

Logikk per par:
  - Begge har samme UUID        → ok, ingenting gjøres
  - nb har UUID, en mangler     → kopier UUID fra nb til en
  - en har UUID, nb mangler     → kopier UUID fra en til nb
  - Ingen av dem har UUID       → generer ny UUID, sett begge
  - Forskjellige UUID-er        → bruk nb som fasit, skriv til en (advarsel)

Duplikatsjekk (kjøres etter hovedløkken):
  - Samme UUID i to forskjellige mapper → regenerer for kopien
    (kopien identifiseres som mappen med færrest git-commits på nb-filen)

Kjøres av GitHub Actions ved push til main.
"""

import os
import re
import subprocess
import sys
import uuid

CONTENT_DIR = "content"

# Matcher en gyldig UUID-verdi på en id:-linje
_UUID_RE = re.compile(
    r'^id:\s*["\']?'
    r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    r'["\']?\s*$',
    re.MULTILINE | re.IGNORECASE,
)

# Matcher en hvilken som helst id:-linje (for erstatning)
_ID_LINE_RE = re.compile(r'^id:.*$', re.MULTILINE)

# Matcher YAML-frontmatter-blokk (mellom --- og ---)
_FM_RE = re.compile(r'\A---\n(.*?)\n---\n', re.DOTALL)


def _split(content):
    """Splitter fil i (frontmatter_str, body_str). Returnerer (None, content) hvis ingen frontmatter."""
    m = _FM_RE.match(content)
    return (m.group(1), content[m.end():]) if m else (None, content)


def get_uuid(content):
    """Leser UUID fra frontmatter. Returnerer None hvis ikke funnet."""
    if not content:
        return None
    fm, _ = _split(content)
    m = _UUID_RE.search(fm or "")
    return m.group(1).lower() if m else None


_ID_COMMENT_NB = "# id: auto-generert – kopierte verdier overskrives automatisk ved push"
_ID_COMMENT_EN = "# id: auto-generated – copied values are overwritten automatically on push"


def _id_comment(path):
    return _ID_COMMENT_EN if str(path).endswith('.en.md') else _ID_COMMENT_NB


def set_uuid(path, uid, content):
    """Skriver UUID til frontmatter og lagrer filen."""
    comment = _id_comment(path)
    fm, body = _split(content)
    if fm is None:
        # Ingen frontmatter – legg til med kommentar
        new_content = f"---\n{comment}\nid: {uid}\n---\n{content}"
    elif _ID_LINE_RE.search(fm):
        # Erstatt eksisterende id:-linje (behold ev. kommentar over den)
        new_fm = _ID_LINE_RE.sub(f"id: {uid}", fm, count=1)
        new_content = f"---\n{new_fm}\n---\n{body}"
    else:
        # Sett inn id som første felt i frontmatter med kommentar
        new_content = f"---\n{comment}\nid: {uid}\n{fm}\n---\n{body}"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)


def get_commit_count(path):
    """Teller antall git-commits for en fil. Returnerer 0 ved feil."""
    result = subprocess.run(
        ['git', 'log', '--oneline', '--', path],
        capture_output=True, text=True
    )
    return len(result.stdout.strip().splitlines())


def main():
    if not os.path.isdir(CONTENT_DIR):
        print(f"FEIL: Finner ikke '{CONTENT_DIR}'-mappe", file=sys.stderr)
        sys.exit(1)

    changed = []
    warnings = []

    for root, _dirs, files in os.walk(CONTENT_DIR):
        if "_index.nb.md" not in files:
            continue

        nb = os.path.join(root, "_index.nb.md")
        en = os.path.join(root, "_index.en.md")

        try:
            nb_txt = open(nb, encoding="utf-8").read()
        except OSError as e:
            print(f"  FEIL ved lesing av {nb}: {e}", file=sys.stderr)
            continue

        try:
            en_txt = open(en, encoding="utf-8").read()
            en_exists = True
        except FileNotFoundError:
            en_txt = None
            en_exists = False

        nb_id = get_uuid(nb_txt)
        en_id = get_uuid(en_txt)

        if nb_id and en_id:
            if nb_id != en_id:
                warnings.append(
                    f"  ⚠  UUID-konflikt i {root}\n"
                    f"       nb: {nb_id}\n"
                    f"       en: {en_id}\n"
                    f"       → bruker nb som fasit"
                )
                set_uuid(en, nb_id, en_txt)
                changed.append(en)
            # else: begge ok

        elif nb_id and en_exists:
            # en mangler UUID – kopier fra nb
            set_uuid(en, nb_id, en_txt)
            changed.append(en)
            print(f"  + Kopiert UUID til en: {en}")

        elif en_id:
            # nb mangler UUID – kopier fra en
            set_uuid(nb, en_id, nb_txt)
            changed.append(nb)
            print(f"  + Kopiert UUID til nb: {nb}")

        else:
            # Ingen av dem har UUID – generer ny
            new_id = str(uuid.uuid4())
            set_uuid(nb, new_id, nb_txt)
            changed.append(nb)
            print(f"  + Ny UUID: {root}")
            if en_exists:
                set_uuid(en, new_id, en_txt)
                changed.append(en)

    for w in warnings:
        print(w)

    # --- Duplikatsjekk ---
    # Samle alle UUID-er på tvers av mapper for å oppdage kopierte mapper.
    uuid_to_roots = {}
    for root, _dirs, files in os.walk(CONTENT_DIR):
        if "_index.nb.md" not in files:
            continue
        nb = os.path.join(root, "_index.nb.md")
        try:
            nb_txt = open(nb, encoding="utf-8").read()
        except OSError:
            continue
        nb_id = get_uuid(nb_txt)
        if nb_id:
            uuid_to_roots.setdefault(nb_id, []).append(root)

    for uid, roots in uuid_to_roots.items():
        if len(roots) <= 1:
            continue

        # Finn originalen: mappen med flest git-commits på nb-filen.
        with_counts = sorted(
            [(get_commit_count(os.path.join(r, "_index.nb.md")), r) for r in roots],
            reverse=True
        )
        original = with_counts[0][1]
        for _count, root in with_counts[1:]:
            new_id = str(uuid.uuid4())
            print(
                f"  ⚠  Duplikat UUID {uid} i {root}\n"
                f"       Original: {original}\n"
                f"       → regenerert ny UUID: {new_id}"
            )
            nb = os.path.join(root, "_index.nb.md")
            nb_txt = open(nb, encoding="utf-8").read()
            set_uuid(nb, new_id, nb_txt)
            changed.append(nb)
            en = os.path.join(root, "_index.en.md")
            if os.path.isfile(en):
                en_txt = open(en, encoding="utf-8").read()
                set_uuid(en, new_id, en_txt)
                changed.append(en)

    if changed:
        print(f"\n✔ Oppdaterte {len(changed)} fil(er) med UUID")
    else:
        print("✔ Alle UUID-er er på plass – ingen endringer")


if __name__ == "__main__":
    main()
