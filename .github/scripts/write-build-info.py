#!/usr/bin/env python3
"""
Skriv public/build.json – kvittering på hvilke commits som er med i bygget.

Nettleseren poller filen etter en lagring og vet at endringen er publisert
når commiten den laget står i lista for repoet. Da trengs ikke GitHubs
kjørestatus, som kan henge i minutter (solution-samt-bu-docs#77).

Hver repo får de siste HISTORY commitene, slik at en nyere commit oppå
brukerens også teller som «med». Filen deployes sammen med resten av
nettstedet, så den blir synlig samtidig med sidene.

Kjøres i CI etter hugo-bygget. Feiler aldri bygget: mangler historikken
for en modul, får den en tom liste.

Bruk: write-build-info.py [utfil]   (standard: public/build.json)
Miljø: GITHUB_RUN_ID, GITHUB_TOKEN (valgfri, gir høyere API-grense),
       BUILD_FALLBACK_REPORT (valgfri, filer satt til side, gir set_aside)
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

HISTORY = 30
ORG = 'SAMT-X'
MAIN_REPO = 'samt-bu-docs'
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Pseudo-versjon fra hugo mod get: v0.0.0-20261024144739-1f5affbe5a4c
GO_MOD_LINE = re.compile(r'github\.com/' + ORG + r'/([\w.-]+)\s+v\S*-([0-9a-f]{12})\b', re.IGNORECASE)


def local_history():
    out = subprocess.run(['git', '-C', ROOT, 'log', '-%d' % HISTORY, '--format=%H'],
                         capture_output=True, text=True, check=True).stdout
    return out.split()


def module_versions():
    with open(os.path.join(ROOT, 'go.mod'), encoding='utf-8') as f:
        return {m.group(1).lower(): m.group(2) for m in GO_MOD_LINE.finditer(f.read())}


def remote_history(repo, sha):
    url = 'https://api.github.com/repos/%s/%s/commits?sha=%s&per_page=%d' % (ORG, repo, sha, HISTORY)
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json'})
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        req.add_header('Authorization', 'Bearer ' + token)
    with urllib.request.urlopen(req, timeout=20) as r:
        return [c['sha'] for c in json.load(r)]


def set_aside():
    """Filer som build-with-fallback.py satte til side i dette bygget (solution-samt-bu-docs#83)."""
    path = os.environ.get('BUILD_FALLBACK_REPORT')
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return [{'repo': r['repo'], 'path': r['path']} for r in json.load(f)]


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'public', 'build.json')
    repos = {MAIN_REPO: local_history()}
    for repo, sha in sorted(module_versions().items()):
        try:
            repos[repo] = remote_history(repo, sha)
        except Exception as e:
            print('Advarsel: fant ikke historikk for %s (%s): %s' % (repo, sha, e))
            repos[repo] = []
    info = {
        'run_id': int(os.environ.get('GITHUB_RUN_ID') or 0),
        'built_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'repos': repos,
        'set_aside': set_aside(),
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=1)
    for repo, shas in repos.items():
        print('%-28s %s' % (repo, shas[0][:7] if shas else '(tom)'))


if __name__ == '__main__':
    main()
