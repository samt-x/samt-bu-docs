---
title: "Platform choice: GitHub"
linkTitle: "Platform choice: GitHub"
weight: 5

---

SAMT-BU uses GitHub for content, tasks and collaboration. This page explains why, what the choice costs in terms of digital sovereignty, and what it would take to choose differently. Other pages in the documentation refer here instead of repeating the rationale.

**Status: provisional choice.** GitHub has been used since the documentation work started in February 2026. The choice is recorded in the [decision log](/en/prosjektstyring/beslutningslogg/2026-10-11-plattformvalg-github/) and can be revisited.

## What GitHub is used for

| Use | Example |
|---|---|
| Content | All pages on docs.samt-bu.no are text files in repositories in the samt-x organisation |
| Tasks | Issues and project boards, see [Task management](/en/prosjektleveranser/loesninger/styringsloesninger/oppgavestyring/) |
| Editing on the website | Login, saving and change suggestions go through GitHub, see [SAMT-BU Docs](/en/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/) |
| Building and publishing | GitHub Actions builds the website on every change, and Cloudflare Pages publishes it |
| Access | Teams in the organisation control who can change what |

## Why GitHub

- **That is where the partners are.** GitHub is the most widely used platform in Digdir and among the partners. Altinn, the National Data Catalogue and most visible open source projects in the Norwegian public sector are there.
- **No barrier to getting started.** Many participants already have an account, and use is free for public repositories.
- **Mature ecosystem.** Tools, integrations and documentation exist for almost everything the project needs.

The choice is pragmatic, not necessarily the architecturally strongest.

## What the choice costs: digital sovereignty

GitHub is owned by Microsoft and subject to US law, including the CLOUD Act. GitHub is not open source, and cannot be self-hosted on Norwegian or European infrastructure without a licence from Microsoft.

For a public sector project this means that

- the project's workspace depends on a single commercial vendor outside the EU/EEA
- terms, prices and features can change without the project having any influence
- the content is public today, but non-public or sensitive content should not be placed there without a separate assessment

The same applies to **Cloudflare**, which publishes the website and handles login. Cloudflare is also a US company. Changing the git platform therefore does not by itself solve the sovereignty question for the website. Publishing must be assessed separately.

As long as the content is open and can be moved, we consider the risk acceptable. That is why the choice is provisional.

## The docs solution and the platform choice

The website docs.samt-bu.no is the part of the project most closely tied to the platform choice. It consists of layers with very different degrees of lock-in:

| Layer | Tied to | Can it be moved? |
|---|---|---|
| Content (Markdown files) and building (Hugo) | Nothing | **Yes**, unchanged |
| Content modules | Addresses of the form github.com/SAMT-X/… | **Yes**, the addresses are changed |
| Editing, change suggestions and handling of suggestions | GitHub's programming interface, about 36 calls in the theme | **Must be rewritten** |
| Login | A GitHub App and a Cloudflare Worker | **Must be rewritten.** With GitLab, the Worker is probably not needed. |
| Publishing | Cloudflare Pages | **A separate choice**, can be changed independently of the git platform |

The built-in editor was made for the project and lets participants without Git knowledge contribute. It is also the biggest lock-in. See [SAMT-BU Docs](/en/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/) for how the solution is built.

## Alternatives

The way of working – content as text in git, tasks as issues, changes as suggestions – is not tied to GitHub. The same way of working exists in other git-based solutions:

| Solution | Characteristics |
|---|---|
| **GitLab** | Same model as GitHub. The Community Edition is open source and can be self-hosted. Has hierarchical access control (groups and subgroups) suited to projects with many sub-projects. The European Commission runs [code.europa.eu](https://code.europa.eu/) on GitLab. Note that the GitLab.com service is also run by a US company. The sovereignty benefit only comes with self-hosting or hosting by a European operator. |
| **Forgejo** | A lighter open source solution, made for self-hosting and governed by a community. |
| **Codeberg** | A European non-profit service built on Forgejo. |

For similar projects in the public sector, a solution that can be self-hosted should be considered the first choice.

## What it would take to switch

| Part | Can it be moved? |
|---|---|
| The content (text files and history) | **Yes**, unchanged. Git is the same everywhere. |
| Tasks (issues and comments) | **Partly.** GitLab has a built-in import from GitHub, but links and numbers change. |
| Project boards | **No.** Must be rebuilt. Some GitLab features require a paid edition. |
| Editing and login on the website | **No.** Must be rewritten, see [The docs solution](#the-docs-solution-and-the-platform-choice). |
| Build scripts | **Partly.** GitHub Actions must be translated to GitLab CI. The scripts are short. |

The content, which is what matters most, is not locked in. What is locked in is the tooling around it.

### How big would a switch be?

A switch has two parts, and they have changed differently.

**The technical part has become considerably smaller.** With AI-assisted development, rewriting the editor against a new programming interface, translating build scripts and moving content is a bounded job. The concepts are the same: GitLab has commits, branches and merge requests where GitHub has pull requests. As a rough estimate, it is a matter of days to a couple of weeks of focused work, not months. **The estimate has not been tested.**

**The organisational part is unchanged, and is now the largest:**

- **Who will operate it?** Sovereignty requires self-hosting or a European operator. That is a decision and a cost outside the project.
- **All participants need new accounts** and must learn a new place to work. Many of them are not technical.
- **Lessons must be learned again.** For example how notifications work, the access model and the risk assessment.
- **Timing:** A switch in the middle of a project with several active pilots is a risk in itself.

A switch is therefore still a major undertaking, but the bottleneck is no longer the code.

**How the estimate can be made reliable:** A bounded trial of two to three days, in which one content repository is mirrored to GitLab and login and saving are ported for that repository. That would give us a figure we can stand behind, instead of an estimate.

## When the choice should be revisited

- The project is to handle non-public or sensitive content
- The commissioning body or Digdir sets requirements for digital sovereignty or hosting in Norway or the EU
- The project's results are to move into permanent management
- A shared public sector git platform becomes available
- GitHub changes its terms or prices significantly

## More on the topic

- [Co-creation → Task management](/en/utkast/temaer/samskaping/oppgavestyring/) discusses why git-based platforms suit collaboration between equal organisations
- [Concept for GitHub Organizations and Repositories](/en/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/github-struktur/) describes how the samt-x organisation is set up
