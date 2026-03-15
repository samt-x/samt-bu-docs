---
id: "1e0d2050-f885-496d-8ab4-8bdc287697e8"
title: "How to Contribute"
linkTitle: "How to Contribute"
weight: 30
last_editor: Erik Hagen

---

This website is open to contributions from all partners in the SAMT-BU project. There are three ways to contribute, depending on the type of changes you want to make and your technical background:

| Method | Suitable for | Requires |
|--------|-------------|---------|
| [CMS editing](#option-1--editing-in-the-browser-via-cms) | Subject-matter experts and editors | GitHub account (free) |
| [GitHub editing](#option-2--editing-directly-on-github) | Minor changes, technical users | GitHub account + Markdown |
| [Local setup](#option-3--local-setup-for-developers) | Structural changes, developers | Hugo + Git installed |

---

## Option 1 – Editing in the Browser via CMS

**This is the recommended option for most contributors.** You edit content directly in the browser using a visual editor – no knowledge of Markdown or Git required.

**To edit an existing page:**

1. Go to the page you wish to edit on the website
2. Click the **"Edit"** menu in the top-right corner of the header
3. Select **"This page"** – you are taken directly to the correct page in the CMS editor
4. Log in with your GitHub account (first time: click "Login with GitHub")
5. Make your changes in the editing field
6. Click **"Save"** – the change is published automatically after a short while

**To create a new page:**

1. Click **"Edit"** → **"Other options"** in the header to open the CMS portal
2. Select the appropriate collection in the left panel
3. Click **"New"** and fill in the title and content
4. Click **"Save"**

> **Note:** You need a GitHub account to log in. Create one for free at [github.com](https://github.com). Contact an administrator to obtain write access to the correct repository the first time.

---

## Option 2 – Editing Directly on GitHub

Suitable for individual changes and minor corrections without a local installation. Requires a GitHub account and familiarity with Markdown.

**How to do it:**

1. Go to the page you wish to edit at [samt-x.github.io/samt-bu-docs](https://samt-x.github.io/samt-bu-docs/)
2. Click the **"Edit on GitHub"** link at the bottom of the page
3. Make your changes in the Markdown field
4. Scroll down to **"Commit changes"**
5. Write a brief description of what you changed
6. Select **"Create a new branch and start a pull request"** (recommended), or commit directly to `main` if you have the necessary permissions
7. Click **"Propose changes"** – an editor will review and approve it

The page is published automatically within a minute of the change being approved.

---

## Option 3 – Local Setup (for Developers)

This option gives you a full local working environment in which you can preview all changes in the browser as you write. Recommended for structural changes, larger amounts of new content, or technical development.

### What You Need

| Tool | Version | Purpose |
|------|---------|---------|
| [Git](https://git-scm.com/) | Latest stable | Version control |
| [Hugo Extended](https://gohugo.io/) | 0.155.3 or later | Site generator |
| [Go](https://go.dev/) | 1.21 or later | Required by Hugo Modules |
| Text editor | – | [VS Code](https://code.visualstudio.com/) recommended |

### Installation on Windows

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

### Installation on macOS

```bash
brew install git hugo go
```

### Installation on Linux (Ubuntu/Debian)

```bash
sudo apt install git golang
# Hugo Extended is obtained from GitHub Releases (the apt version is often too old):
wget https://github.com/gohugoio/hugo/releases/download/v0.155.3/hugo_extended_0.155.3_linux-amd64.deb
sudo dpkg -i hugo_extended_0.155.3_linux-amd64.deb
```

### Clone the Repository

```bash
git clone --recurse-submodules https://github.com/SAMT-X/samt-bu-docs.git
cd samt-bu-docs
hugo mod download
```

`--recurse-submodules` ensures that the theme (`hugo-theme-samt-bu`) is downloaded at the same time. `hugo mod download` fetches content modules from the other repositories.

### Start Local Preview

```bash
hugo server
```

Open [http://localhost:1313/samt-bu-docs/](http://localhost:1313/samt-bu-docs/) in the browser. The page updates automatically when you save a file.

### File Structure – Where the Content Lives

```
content/
  om/                    ← "About" section
  behov/                 ← Needs (use cases)
  pilotering/            ← Pilots
  arkitektur/            ← Architecture
  loesning/              ← Solutions
  rammeverk/             ← Framework
  informasjonsmodeller/  ← Information Models
  innsikt/               ← Shared Insight
  teams/                 ← Teams (content module)
  utkast/                ← Drafts and inputs (content module)
```

Each chapter is a **folder** containing two files:

```
content/om/om-samt-bu/
  _index.nb.md    ← Norwegian content
  _index.en.md    ← English content
```

### Writing Content

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

### Saving and Publishing Changes

```bash
git add content/path/to/file/_index.en.md
git commit -m "Brief description of what you changed"
git push
```

GitHub Actions builds and publishes automatically after 1–2 minutes.

> **No write access to the repository?** Create a *pull request* instead:
> `git checkout -b my-contribution` → make changes → `git push origin my-contribution` → open a PR on GitHub.

### Useful Commands

| Command | Description |
|---------|-------------|
| `hugo server` | Start local server with live reload |
| `hugo server -D` | Include pages marked with `draft: true` |
| `hugo` | Build to the `public/` folder (check for errors) |
| `git pull` | Fetch the latest changes from GitHub |
| `hugo mod get -u` | Update all content modules to the latest version |
