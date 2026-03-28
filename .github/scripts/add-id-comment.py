#!/usr/bin/env python3
"""
Legg til/oppdater forklaringskommentar over id:-feltet i alle frontmatter-filer.
Bruker norsk kommentar for .nb.md og engelsk for .en.md.
Kjøres én gang – ensure-uuids.py håndterer nye filer fremover.

Kjør fra rot av samt-bu-docs:
  py .github/scripts/add-id-comment.py
"""
import os
import re

REPOS = [
    'S:/app-data/github/samt-x-repos/samt-bu-docs/content',
    'S:/app-data/github/samt-x-repos/team-architecture/content',
    'S:/app-data/github/samt-x-repos/team-semantics/content',
    'S:/app-data/github/samt-x-repos/samt-bu-drafts/content',
    'S:/app-data/github/samt-x-repos/solution-samt-bu-docs/content',
    'S:/app-data/github/samt-x-repos/team-pilot-1/content',
]

ID_COMMENT_NB = "# id: auto-generert – kopierte verdier overskrives automatisk ved push"
ID_COMMENT_EN = "# id: auto-generated – copied values are overwritten automatically on push"

# Matcher enhver id-kommentarlinje (begge språk)
_ANY_ID_COMMENT_RE = re.compile(r'^# id: auto-gen\w.*\n', re.MULTILINE)


def get_comment(filepath):
    return ID_COMMENT_EN if filepath.endswith('.en.md') else ID_COMMENT_NB


def add_id_comment(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return False
    end = content.find('\n---', 3)
    if end == -1:
        return False

    frontmatter = content[3:end]

    if not re.search(r'^id:', frontmatter, re.MULTILINE):
        return False  # ingen id-felt

    correct_comment = get_comment(filepath)

    if correct_comment in frontmatter:
        return False  # riktig kommentar finnes allerede

    # Fjern evt. feil-språklig kommentar, legg til riktig
    new_fm = _ANY_ID_COMMENT_RE.sub('', frontmatter)
    new_fm = re.sub(
        r'^(id:)',
        f'{correct_comment}\n\\1',
        new_fm,
        flags=re.MULTILINE,
        count=1
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---' + new_fm + content[end:])
    return True


total = 0
for content_path in REPOS:
    if not os.path.isdir(content_path):
        print(f'Hopper over {content_path} (ikke funnet)')
        continue
    count = 0
    for root, _, files in os.walk(content_path):
        for filename in files:
            if filename.endswith('.md'):
                if add_id_comment(os.path.join(root, filename)):
                    count += 1
    print(f'{content_path}: {count} filer oppdatert')
    total += count

print(f'\nTotalt: {total} filer')
