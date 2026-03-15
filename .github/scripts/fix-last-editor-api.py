#!/usr/bin/env python3
"""
Batch-opprydding av last_editor via GitHub API.

For hver .md-fil hentes commit-historikken fra GitHub API.
Commits som er batch-/metadata-operasjoner hoppes over slik at
den siste EKTE innholdsendringen vises.

Kjør fra rot av samt-bu-docs:
  py .github/scripts/fix-last-editor-api.py
"""
import subprocess
import os
import re
import urllib.request
import urllib.error
import urllib.parse
import json
import time

# Hent token fra gh CLI
token_result = subprocess.run(
    [r'C:\Program Files\GitHub CLI\gh.exe', 'auth', 'token'],
    capture_output=True, text=True
)
TOKEN = token_result.stdout.strip()
if not TOKEN:
    print('Feil: Kunne ikke hente GitHub-token. Er du logget inn med gh?')
    exit(1)

REPOS = [
    ('S:/app-data/github/samt-x-repos/samt-bu-docs',           'content', 'SAMT-X/samt-bu-docs'),
    ('S:/app-data/github/samt-x-repos/team-architecture',      'content', 'SAMT-X/team-architecture'),
    ('S:/app-data/github/samt-x-repos/team-semantics',         'content', 'SAMT-X/team-semantics'),
    ('S:/app-data/github/samt-x-repos/samt-bu-drafts',         'content', 'SAMT-X/samt-bu-drafts'),
    ('S:/app-data/github/samt-x-repos/solution-samt-bu-docs',  'content', 'SAMT-X/solution-samt-bu-docs'),
]

BOT_LOGINS = {'github-actions[bot]', 'dependabot[bot]'}

_user_name_cache = {}

def get_display_name(login):
    """Hent display-navn for en GitHub-bruker (cachet)."""
    if login in _user_name_cache:
        return _user_name_cache[login]
    data = gh_api(f'https://api.github.com/users/{login}')
    name = (data.get('name') or '').strip() if data else ''
    _user_name_cache[login] = name
    time.sleep(0.05)
    return name

# Commit-meldinger som skal hoppes over (batch/metadata-operasjoner)
SKIP_MSG_PATTERNS = [
    'Metadata: last_editor',
    'batch-opprydding',
    'last_editor satt for alle',
    'last_editor oppdatert via GitHub API',
    'Vekter: 10-inkrement',
    'Legg til UUID-identifikator i frontmatter',
    'inject-lastmod med last_editor',
]


def is_batch_commit(message):
    msg = message or ''
    return any(p.lower() in msg.lower() for p in SKIP_MSG_PATTERNS)


def gh_api(url):
    req = urllib.request.Request(
        url,
        headers={
            'Authorization': f'token {TOKEN}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f'    API-feil {e.code}: {url}')
        return None


def get_last_real_editor(github_repo, file_path):
    """Hent siste ikke-batch, ikke-bot GitHub-bruker for filen."""
    page = 1
    while page <= 5:  # maks 5 sider = 100 commits
        url = (f'https://api.github.com/repos/{github_repo}/commits'
               f'?path={urllib.parse.quote(file_path)}&per_page=20&page={page}')
        commits = gh_api(url)
        if not commits:
            break
        for commit in commits:
            msg = commit.get('commit', {}).get('message', '')
            if is_batch_commit(msg):
                continue
            author = commit.get('author')
            if not author:
                continue
            login = author.get('login', '')
            if login in BOT_LOGINS or '[bot]' in login:
                continue
            # Prøv profil-navn fra Users API, fall tilbake til commit-metadata-navn
            profile_name = get_display_name(login)
            commit_name = commit.get('commit', {}).get('author', {}).get('name', '').strip()
            name = profile_name or commit_name
            return login, name
        if len(commits) < 20:
            break  # ingen flere sider
        page += 1
    return None, None


def set_last_editor(filepath, value):
    """Sett last_editor i frontmatter. Returnerer True ved endring."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return False
    end = content.find('\n---', 3)
    if end == -1:
        return False
    frontmatter = content[3:end]
    rest = content[end:]
    if re.search(r'^last_editor:', frontmatter, re.MULTILINE):
        new_fm = re.sub(r'^last_editor:.*$', f'last_editor: {value}',
                        frontmatter, flags=re.MULTILINE)
    else:
        new_fm = frontmatter.rstrip('\n') + f'\nlast_editor: {value}\n'
    if new_fm == frontmatter:
        return False
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---' + new_fm + rest)
    return True


total_updated = 0

for repo_path, content_dir, github_repo in REPOS:
    content_path = os.path.join(repo_path, content_dir)
    if not os.path.isdir(content_path):
        print(f'Hopper over {repo_path} (ikke funnet)')
        continue

    repo_updated = 0
    print(f'\n{github_repo}')

    for root, dirs, files in os.walk(content_path):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, repo_path).replace('\\', '/')

            login, name = get_last_real_editor(github_repo, rel_path)
            time.sleep(0.1)

            if not login:
                print(f'  [ingen ekte editor funnet] {rel_path}')
                continue

            value = f'{login} ({name})' if name and name != login else f'{login} (ukjent navn)'

            if set_last_editor(filepath, value):
                print(f'  OK {rel_path} -> {value}')
                repo_updated += 1
            else:
                print(f'  = {rel_path} (uendret: {value})')

    print(f'  {repo_updated} fil(er) oppdatert')
    total_updated += repo_updated

print(f'\nTotalt oppdatert: {total_updated} fil(er)')
print('Neste steg: git add + commit + push i hvert berort repo')
