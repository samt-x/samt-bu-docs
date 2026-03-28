#!/usr/bin/env python3
"""
Legg til forklaringskommentar over id:-feltet i alle frontmatter-filer.
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

ID_COMMENT = "# id: auto-generert – kopierte verdier overskrives automatisk ved push"


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

    if ID_COMMENT in frontmatter:
        return False  # kommentar finnes allerede

    new_fm = re.sub(
        r'^(id:)',
        f'{ID_COMMENT}\n\\1',
        frontmatter,
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
