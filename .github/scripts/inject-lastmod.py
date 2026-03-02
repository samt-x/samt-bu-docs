#!/usr/bin/env python3
"""
Inject lastmod dates into Hugo module content frontmatter based on git history.
Run in CI before hugo build to get accurate last-modified timestamps for module content.
Does not commit anything – modifies files only in the CI workspace.
"""
import subprocess
import os
import re

MODULE_PATHS = [
    '.hugo-modules/team-architecture',
    '.hugo-modules/samt-bu-drafts',
]


def get_lastmod(module_path, rel_path):
    result = subprocess.run(
        ['git', 'log', '-1', '--format=%cI', '--', rel_path],
        capture_output=True, text=True, cwd=module_path
    )
    return result.stdout.strip()


def inject_lastmod(filepath, lastmod):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return False

    end = content.find('\n---', 3)
    if end == -1:
        return False

    frontmatter = content[3:end]
    rest = content[end:]

    if re.search(r'^lastmod:', frontmatter, re.MULTILINE):
        frontmatter = re.sub(r'^lastmod:.*$', f'lastmod: {lastmod}', frontmatter, flags=re.MULTILINE)
    else:
        frontmatter = frontmatter.rstrip('\n') + f'\nlastmod: {lastmod}\n'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---' + frontmatter + rest)

    return True


for module_path in MODULE_PATHS:
    if not os.path.isdir(module_path):
        print(f'Skipping {module_path} (not found)')
        continue

    print(f'Processing {module_path}...')
    content_path = os.path.join(module_path, 'content')

    for root, dirs, files in os.walk(content_path):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, module_path)

            lastmod = get_lastmod(module_path, rel_path)
            if lastmod:
                if inject_lastmod(filepath, lastmod):
                    print(f'  {rel_path}: lastmod: {lastmod}')
