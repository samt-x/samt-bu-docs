#!/usr/bin/env python3
"""
Kjør hugo-bygget, og sett til side en innholdsfil som stopper det.

Ett ødelagt bygg skal ikke stoppe alle andres endringer
(solution-samt-bu-docs#83). Feiler hugo med en melding som peker på en
innholdsfil ("…/content/x/_index.nb.md:5:1"), legger skriptet tilbake
versjonen som sist ble publisert og bygger på nytt. Siden ser da ut som før,
og alle andre endringer kommer ut. Fila hentes fra commiten som står først
for repoet i den publiserte build.json. Fantes ikke fila da, holdes den
utenfor bygget.

Endringen gjøres bare i CI-arbeidsområdet (og i modulcachen), aldri i git.

- Hugo melder én feil om gangen, så skriptet prøver høyst MAX_SET_ASIDE filer.
- Feil i maler, tema og konfigurasjon peker ikke på innhold. Da gis det opp,
  og bygget feiler som før.
- Rapporten (JSON-liste) skrives til REPORT, og til jobbsammendraget.

Bruk: build-with-fallback.py <hugo-kommando …>
Miljø: BUILD_FALLBACK_REPORT (rapportfil), GITHUB_TOKEN (valgfri),
       GITHUB_STEP_SUMMARY (settes av Actions)
"""
import json
import os
import re
import stat
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

MAX_SET_ASIDE = 3
ORG = 'SAMT-X'
MAIN_REPO = 'samt-bu-docs'
SITE_BUILD_INFO = 'https://docs.samt-bu.no/build.json'
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# "…/content/x/_index.nb.md:6:19": melding
ERROR_FILE = re.compile(r'"([^"\n]+?\.(?:md|markdown)):(\d+):(\d+)"')
# Modulcachen: …/github.com/!s!a!m!t-!x/samt-bu-pilot-1@v0.0.0-…/content/x.md
MODULE_FILE = re.compile(r'github\.com/!s!a!m!t-!x/([\w.-]+)@[^/]+/(.+)$', re.IGNORECASE)


def run_hugo(cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.stdout.write(p.stderr)
    sys.stdout.flush()
    return p.returncode, p.stdout + p.stderr


def failing_file(output):
    """(sti, repo, sti i repoet, feilmelding) for første innholdsfil i feilen, ellers None."""
    for m in ERROR_FILE.finditer(output):
        path = os.path.normpath(m.group(1))
        norm = path.replace('\\', '/')
        line = output[m.start():].split('\n', 1)[0]
        root_content = os.path.join(ROOT, 'content').replace('\\', '/') + '/'
        if norm.startswith(root_content):
            return path, MAIN_REPO, norm[len(ROOT.replace('\\', '/')) + 1:], line
        mm = MODULE_FILE.search(norm)
        if mm and mm.group(2).startswith('content/'):
            return path, mm.group(1).lower(), mm.group(2), line
    return None


def published_shas():
    """({repo: publisert commit}, {(repo, sti): commit} for filer som alt er satt til side).

    En fil som ble satt til side i forrige bygg, er ødelagt også i commiten som da
    ble publisert. Den skal fortsatt hentes fra commiten versjonen opprinnelig kom fra.
    """
    # Cloudflare avviser Pythons standard User-Agent med 403
    req = urllib.request.Request(SITE_BUILD_INFO + '?_=' + str(os.getpid()),
                                 headers={'User-Agent': 'samt-bu-docs-ci'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            info = json.load(r)
    except Exception as e:
        print('Advarsel: fant ikke publisert build.json: %s' % e)
        return {}, {}
    heads = {k.lower(): v[0] for k, v in info.get('repos', {}).items() if v}
    earlier = {(s['repo'], s['path']): s['published_sha']
               for s in info.get('set_aside', []) if s.get('published_sha')}
    return heads, earlier


def published_version(repo, rel, sha):
    """Innholdet i fila ved commiten sha. None = fila fantes ikke. Unntak = vet ikke."""
    if repo == MAIN_REPO:
        p = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (sha, rel)], capture_output=True)
        if p.returncode == 0:
            return p.stdout
        if b'does not exist' in p.stderr or b'exists on disk, but not in' in p.stderr:
            return None
        raise RuntimeError(p.stderr.decode('utf-8', 'replace').strip())
    url = 'https://api.github.com/repos/%s/%s/contents/%s?ref=%s' % (
        ORG, repo, urllib.parse.quote(rel), sha)
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.raw+json'})
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        req.add_header('Authorization', 'Bearer ' + token)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def make_writable(path):
    # Go legger modulcachen skrivebeskyttet
    for p in (os.path.dirname(path), path):
        if os.path.exists(p):
            os.chmod(p, os.stat(p).st_mode | stat.S_IWUSR)


def write_report(report):
    out = os.environ.get('BUILD_FALLBACK_REPORT')
    if out:
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=1, ensure_ascii=False)
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary and report:
        with open(summary, 'a', encoding='utf-8') as f:
            f.write('## Filer satt til side i dette bygget\n\n')
            f.write('Bygget feilet på disse filene. De er erstattet med forrige publiserte versjon '
                    '(eller holdt utenfor), og resten av nettstedet er bygget (solution-samt-bu-docs#83).\n\n')
            for r in report:
                f.write('- `%s` i `%s` – %s\n  `%s`\n' % (r['path'], r['repo'], r['action'], r['error']))


def main():
    cmd = sys.argv[1:]
    if not cmd:
        sys.exit('Bruk: build-with-fallback.py <hugo-kommando …>')
    report = []
    shas = None
    while True:
        code, output = run_hugo(cmd)
        if code == 0:
            write_report(report)
            return 0
        found = failing_file(output)
        if not found:
            print('\nFeilen peker ikke på en innholdsfil – ingenting å sette til side.')
            break
        path, repo, rel, line = found
        if any(r['repo'] == repo and r['path'] == rel for r in report):
            print('\n%s feiler fortsatt etter at den ble satt til side – gir opp.' % rel)
            break
        if len(report) >= MAX_SET_ASIDE:
            print('\nFor mange filer feiler (%d satt til side) – gir opp.' % len(report))
            break
        if shas is None:
            shas, earlier = published_shas()
        sha = earlier.get((repo, rel)) or shas.get(repo)
        if not sha:
            print('\nVet ikke hvilken commit som er publisert for %s – gir opp.' % repo)
            break
        try:
            content = published_version(repo, rel, sha)
        except Exception as e:
            print('\nFant ikke publisert versjon av %s: %s – gir opp.' % (rel, e))
            break
        make_writable(path)
        if content is None:
            os.remove(path)
            action = 'holdt utenfor (fantes ikke i forrige bygg)'
        else:
            with open(path, 'wb') as f:
                f.write(content)
            action = 'forrige publiserte versjon (%s)' % sha[:7]
        print('\n>>> Setter til side %s i %s: %s. Bygger på nytt.\n' % (rel, repo, action))
        report.append({'repo': repo, 'path': rel, 'published_sha': sha,
                       'action': action, 'error': line.strip()})
    write_report(report)
    return 1


if __name__ == '__main__':
    sys.exit(main())
