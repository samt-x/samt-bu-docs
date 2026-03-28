---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: "1e0d2050-f885-496d-8ab4-8bdc287697e8"
title: "How to Contribute"
linkTitle: "How to Contribute"
weight: 30

---

This website is open to contributions from all partners in the SAMT-BU project. There are several ways to contribute – see the overview below. For most subject-matter experts and editors, the **built-in browser editor** is the recommended starting point.

| Method | Suitable for | Requires |
|--------|-------------|---------|
| [Built-in editor](#recommended-built-in-editing-in-the-browser) | Subject-matter experts and editors | GitHub account + write access |
| [GitHub editing](#alternative-editing-directly-on-github) | Minor changes, technical users | GitHub account + Markdown |
| [Local setup](#alternative-local-setup-for-developers) | Structural changes, developers | Hugo + Git installed |

---

## Recommended: Built-in Editing in the Browser

You edit content directly in the browser using a visual text editor – no knowledge of Markdown or Git required.

### What You Need

- A **GitHub account** (create one for free at [github.com](https://github.com))
- **Write access** to the correct repository – contact an administrator to obtain this the first time

### Editing an Existing Page

1. Go to the page you wish to edit
2. Click the **"Edit"** menu in the top-right corner of the header
3. Select **"Edit this chapter"**
4. Log in with your GitHub account if you are not already logged in (pop-up window)
5. Make your changes in the text field
6. Click **"Save"**

**Tip:** Images can be pasted directly into the text field (Ctrl+V or right-click → Paste) – there is currently no dedicated image button in the toolbar.

The website updates automatically after saving. A status indicator at the bottom left of the screen keeps you informed throughout.

### Status indicator and build history

**The indicator at the bottom left** is always visible and shows the current state:

| State | Text | Meaning |
|-------|------|---------|
| No active job | «Build history» | Click to see previous build jobs |
| Saved, waiting for build | «N changes being built…» | Change sent – build is running or queued |
| Done | «Changes published – click to reload» | Click to view the updated page |

Clicking the indicator opens a **build history dialog** showing recent build jobs with status, timestamp, and a link to GitHub Actions. Here you can see:
- 🔄 Running job – with the number of seconds since it started
- 🕐 Job in queue – waiting its turn
- ✅ Completed
- ✅ (grey) Superseded by a newer build – see explanation below

#### About build times and queues

The site is built by GitHub Actions. A build normally takes **about 1 minute**. If you or others save several pages in quick succession, the wait time may be longer because build jobs run one at a time:

- **2 saves in a row:** the second job waits until the first is done – total time approx. 2 min
- **3 or more rapid saves:** GitHub may *supersede* older queued jobs with the newest one. This means a job in the history may appear as «Superseded» rather than completed – this is normal and does not mean anything went wrong. All saved changes are recorded in Git and will be published by the last job that runs.

> **In short:** If you see a grey tick and the text «Superseded» in the build history, your change has not been lost – it was published by a newer job.

### Creating a New Page

1. Navigate to the page you want to place the new page next to (sibling) or beneath (sub-chapter)
2. Click **"Edit"** and select:
   - **"New chapter after this"** – new page at the same level
   - **"New sub-chapter"** – new page one level down
3. Fill in the title and any content in the dialog
4. Click **"Save"**

> **Note:** Work is ongoing to provide a better overview of active editing across users. The solution is fully usable as it stands today, but pages may take approximately 1 minute to update after saving, and it may not always be visible whether others are editing the same page at the same time.

---

## Alternative: Editing Directly on GitHub

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

## Alternative: Local Setup (for Developers)

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

---

## More detailed user guide

A more comprehensive user guide – including tips for editors, advanced editing, and site administration – is available in the solution documentation:

→ [User guide for SAMT-BU Docs](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/brukerveiledning/)
