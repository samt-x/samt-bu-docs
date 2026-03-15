#!/usr/bin/env python3
"""
Batch-opprydding av last_editor i frontmatter.

Kjøres én gang lokalt for å rette opp sider der last_editor mangler
eller er satt til en bot (github-actions[bot] e.l.).

For hver .md-fil:
  - Finn siste ikke-bot-commit-autor fra git log
  - Sett last_editor hvis feltet mangler eller er en bot-verdi
  - Behold eksisterende menneskelige verdier urørt

Kjør fra rot av samt-bu-docs:
  python .github/scripts/fix-last-editor.py
"""
import subprocess
import os
import re

# Repoer å behandle: (sti til repo-rot, sti til content-mappe relativ til rot)
REPOS = [
    ('S:/app-data/github/samt-x-repos/samt-bu-docs',            'content'),
    ('S:/app-data/github/samt-x-repos/team-architecture',       'content'),
    ('S:/app-data/github/samt-x-repos/team-semantics',          'content'),
    ('S:/app-data/github/samt-x-repos/samt-bu-drafts',          'content'),
    ('S:/app-data/github/samt-x-repos/solution-samt-bu-docs',   'content'),
]


def get_last_human_author(repo_path, rel_path):
    """Finn siste ikke-bot-commit-autor. Returnerer 'login (navn)' eller 'navn'."""
    result = subprocess.run(
        ['git', 'log', '--format=%aN|%aE', '--', rel_path],
        capture_output=True, text=True, cwd=repo_path
    )
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        name, _, email = line.partition('|')
        name, email = name.strip(), email.strip()
        if '[bot]' in name or '[bot]' in email:
            continue
        m = re.match(r'^\d+\+(.+)@users\.noreply\.github\.com$', email)
        if m:
            return f'{m.group(1)} ({name})'
        return name
    return None


def fix_last_editor(filepath, author):
    """Sett last_editor i frontmatter hvis mangler eller er bot-verdi. Returnerer True ved endring."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return False
    end = content.find('\n---', 3)
    if end == -1:
        return False

    frontmatter = content[3:end]
    rest = content[end:]

    existing = re.search(r'^last_editor:\s*(.*)$', frontmatter, re.MULTILINE)
    if existing:
        current_val = existing.group(1).strip()
        if '[bot]' not in current_val and current_val:
            return False  # menneskelig verdi – behold
        # Bot-verdi eller tom – erstatt
        frontmatter = re.sub(
            r'^last_editor:.*$', f'last_editor: {author}',
            frontmatter, flags=re.MULTILINE
        )
    else:
        frontmatter = frontmatter.rstrip('\n') + f'\nlast_editor: {author}\n'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---' + frontmatter + rest)
    return True


total_updated = 0

for repo_path, content_dir in REPOS:
    content_path = os.path.join(repo_path, content_dir)
    if not os.path.isdir(content_path):
        print(f'Hopper over {repo_path} (content-mappe ikke funnet)')
        continue

    repo_updated = 0
    print(f'\n{repo_path}')

    for root, dirs, files in os.walk(content_path):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, repo_path).replace('\\', '/')

            author = get_last_human_author(repo_path, rel_path)
            if not author:
                print(f'  [ingen menneskelig commit] {rel_path}')
                continue

            if fix_last_editor(filepath, author):
                print(f'  OK {rel_path} -> {author}')
                repo_updated += 1

    print(f'  {repo_updated} fil(er) oppdatert')
    total_updated += repo_updated

print(f'\nTotalt oppdatert: {total_updated} fil(er)')
print('Neste steg: git add + commit + push i hvert berørt repo')
