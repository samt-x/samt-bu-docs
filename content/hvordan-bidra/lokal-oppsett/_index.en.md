---
# id: auto-generated – copied values are overwritten automatically on push
id: "e26cb201-0841-46b2-8ac7-2ba3708edde6"
title: "Local Setup (for Developers)"
linkTitle: "Local setup"
weight: 30

---

This option gives you a full local working environment in which you can preview all changes in the browser as you write. Recommended for structural changes, larger amounts of new content, or technical development.

## What You Need

| Tool | Version | Purpose |
|------|---------|---------|
| [Git](https://git-scm.com/) | Latest stable | Version control |
| [Hugo Extended](https://gohugo.io/) | 0.155.3 or later | Site generator |
| [Go](https://go.dev/) | 1.21 or later | Required by Hugo Modules |
| Text editor | – | [VS Code](https://code.visualstudio.com/) recommended |

## Installation on Windows

```powershell
winget install --id Git.Git
winget install --id Hugo.Hugo.Extended
winget install --id GoLang.Go
winget install --id Microsoft.VisualStudioCode
```

Restart the terminal afterwards so that the newly installed programmes are available in PATH.

**Verify the installation:**

```powershell
git --version
hugo version
go version
```

## Installation on macOS

```bash
brew install git hugo go
```

## Installation on Linux (Ubuntu/Debian)

```bash
sudo apt install git golang
# Hugo Extended is obtained from GitHub Releases (the apt version is often too old):
wget https://github.com/gohugoio/hugo/releases/download/v0.155.3/hugo_extended_0.155.3_linux-amd64.deb
sudo dpkg -i hugo_extended_0.155.3_linux-amd64.deb
```

## Content structure – multiple repositories

SAMT-BU Docs uses **content modules**: content from different teams and pilots lives in separate GitHub repositories and is mounted automatically into the site at publication time. You do not need to clone all repositories to see the full site – Hugo fetches any missing modules from GitHub automatically.

| Repository | Content | Mounted under |
|------------|---------|---------------|
| `samt-bu-docs` | Main documentation, configuration | *(root)* |
| `samt-bu-pilot-1` | Pilot 1 | `pilotering/pilot-1/` |
| `samt-bu-pilot-2` | Pilot 2 | `pilotering/pilot-2/` |
| `samt-bu-pilot-3` | Pilot 3 | `pilotering/pilot-3/` |
| `samt-bu-pilot-4` | Pilot 4 | `pilotering/pilot-4/` |
| `team-architecture` | Overall architecture | `arkitektur/overordnet-arkitektur/` |
| `team-semantics` | Information architecture | `arkitektur/informasjonsarkitektur/` |
| `samt-bu-drafts` | Drafts and inputs | `utkast/` |
| `solution-samt-bu-docs` | Technical documentation | `prosjektleveranser/…` |

## Scenario A – Preview the full site only

Clone `samt-bu-docs` and start the server. Hugo fetches content from all module repositories automatically.

```bash
git clone --recurse-submodules https://github.com/SAMT-X/samt-bu-docs.git
cd samt-bu-docs
hugo server
```

Open [http://localhost:1313/](http://localhost:1313/) in the browser.

## Scenario B – Edit content in one specific repository

If you only want to edit content in, for example, `samt-bu-pilot-2`, you only need to clone that repository:

```bash
git clone https://github.com/SAMT-X/samt-bu-pilot-2.git
cd samt-bu-pilot-2
# edit files in content/
git add .
git commit -m "Description of the change"
git push
```

The site updates automatically at [docs.samt-bu.no](https://docs.samt-bu.no/) within about one minute. No local Hugo server is required.

## Scenario C – Full local development across all repositories

If you want to edit content in several modules and see the changes live locally, clone all repositories as sibling folders and use the included helper script:

```bash
# Clone all repositories side by side
git clone --recurse-submodules https://github.com/SAMT-X/samt-bu-docs.git
git clone https://github.com/SAMT-X/samt-bu-pilot-1.git
git clone https://github.com/SAMT-X/samt-bu-pilot-2.git
# ... and so on for the modules you want to work with

# Start the local server (the script finds local clones automatically)
cd samt-bu-docs
tools/hugo-local.sh
```

The script reads `hugo.toml`, detects which modules you have cloned locally, and starts Hugo with those pointing to your local files. Modules you have not cloned are still fetched from GitHub.

```
samt-bu-docs/            ← always clone this one
samt-bu-pilot-1/         ← clone the ones you want to edit
samt-bu-pilot-2/
...
```

**Including drafts:**

```bash
tools/hugo-local.sh --drafts
```

## Writing Content

Content files are standard Markdown files with a small header at the top (frontmatter):

```markdown
---
title: "Page title"
weight: 30
---

Your content begins here in standard Markdown.

## Heading

A paragraph with **bold text** and *italic text*.
```

- `title` – page title displayed in the menu and at the top of the page
- `weight` – sort order (lower number = higher in the menu)
- `draft: true` – add this to hide the page from publication until it is ready

## Saving and Publishing Changes

```bash
git add content/path/to/file/_index.en.md
git commit -m "Brief description of what you changed"
git push
```

GitHub Actions builds and publishes automatically after 1–2 minutes.

> **No write access to the repository?** Create a *pull request* instead:
> `git checkout -b my-contribution` → make changes → `git push origin my-contribution` → open a PR on GitHub.

## Useful Commands

| Command | Description |
|---------|-------------|
| `tools/hugo-local.sh` | Start local server with automatic module substitution |
| `tools/hugo-local.sh --drafts` | Include pages marked with `draft: true` |
| `hugo server` | Start local server (fetches modules from GitHub) |
| `hugo` | Build to the `public/` folder (check for errors) |
| `git pull` | Fetch the latest changes from GitHub |
