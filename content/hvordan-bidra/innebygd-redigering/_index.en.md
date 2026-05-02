---
# id: auto-generated – copied values are overwritten automatically on push
id: "c95d738e-1fe5-43ac-94a8-80202e0a2faa"
title: "Built-in Editing in the Browser"
linkTitle: "Built-in editing"
weight: 10
aliases:
  - /en/om/hvordan-bidra/innebygd-redigering/

---

You edit content directly in the browser using a visual text editor – no knowledge of Markdown or Git required. All common editorial tasks are available from the **"Edit"** menu in the top-right corner of the header.

## What You Need

- A **GitHub account** (create one for free at [github.com](https://github.com)) – that is all you need

**Write access is not required.** Without it, your changes are automatically submitted as a *suggestion* (pull request) for an editor to review and approve. With write access, changes are published directly. Either way, the same interface is used – menu labels adjust automatically.

### About GitHub authorisation

The first time you use the editing features, SAMT-BU Docs will request access to your GitHub account via a login popup. SAMT-BU Docs uses a **GitHub App** that only has access to the specific repositories the app is installed on – not other repositories on your account.

#### Revoking authorisation

You can revoke access at any time:

1. Log in to [github.com](https://github.com)
2. Go to **Settings** (click your profile picture in the top right → *Settings*)
3. Select **Applications** in the left menu
4. Click the **Authorized GitHub Apps** tab
5. Find **SAMT-BU Docs** in the list and click **Revoke**

After revoking, you will be asked to log in again the next time you use the editing features.

## Editing an Existing Page

1. Go to the page you wish to edit
2. Click the **"Edit"** menu in the top-right corner of the header
3. Select **"Edit this page"**
4. Log in with your GitHub account if you are not already logged in (pop-up window)
5. Make your changes in the visual editor
6. Click **"Save"**

**Tip:** Images can be pasted directly into the editor (Ctrl+V or right-click → Paste).

If you have write access, the change is published directly. Without write access, a pull request is created automatically – you will receive a link to it after saving.

The website updates automatically after saving. A status indicator at the bottom left of the screen keeps you informed throughout.

## Creating a New Page

1. Navigate to the page you want to place the new page next to (sibling) or beneath (sub-chapter)
2. Click **"Edit"** and select:
   - **"New chapter after this"** – new page at the same level as the current one
   - **"New sub-chapter"** – new page one level down beneath the current one
3. Fill in the title and any content in the dialog
4. Click **"Save"**

## Moving a Chapter

1. Go to the page you want to move
2. Click the **"Edit"** menu in the top-right corner
3. Select **"Move this chapter"** – a dialog opens and the Edit menu is greyed out
4. Navigate in the menu to the desired location
5. Click **"Move here (before)"** to place it before the selected page, or **"Move here (after)"** to place it after

Click **"Cancel"** in the dialog to abort without making changes. The website updates automatically once the move is complete.

## Deleting a Page

1. Go to the page you want to delete
2. Click the **"Edit"** menu in the top-right corner
3. Select **"Delete this page"**
4. Confirm in the dialog

Both language versions of the page (Norwegian and English) are deleted in a single step. The website updates automatically after deletion.

> **Note:** Deletion cannot be immediately reversed through the interface. Contact an administrator if you have accidentally deleted a page.

## Give Feedback

If you have a comment, a correction to report, or a question about a page's content – without wanting to edit directly – you can use the **"Give feedback"** feature:

1. Go to the page in question
2. Click the **"Edit"** menu and select **"Give feedback"**
3. Log in with your GitHub account if you are not already logged in
4. Fill in the title (pre-filled with the page name) and write your comment
5. Optionally add a link to a specific section in the "Specific section" field
6. Click **"Send"**

Your comment is registered as a GitHub Issue linked to the page. You will receive a link to the issue after submitting, and can follow it there.

**Alternatively**, use the **"Comments"** button in the bottom bar to view existing comments on the page and open a new comment dialog from there.

## Status Indicator and Build History

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

### About Build Times and Queues

The site is built by GitHub Actions. A build normally takes **about 1 minute**. If you or others save several pages in quick succession, the wait time may be longer because build jobs run one at a time:

- **2 saves in a row:** the second job waits until the first is done – total time approx. 2 min
- **3 or more rapid saves:** GitHub may *supersede* older queued jobs with the newest one. This means a job in the history may appear as «Superseded» rather than completed – this is normal and does not mean anything went wrong. All saved changes are recorded in Git and will be published by the last job that runs.

> **In short:** If you see a grey tick and the text «Superseded» in the build history, your change has not been lost – it was published by a newer job.
