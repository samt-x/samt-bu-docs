---
# id: auto-generated – copied values are overwritten automatically on push
id: "23a6ec0b-a515-4db0-907c-7d96836d3dfd"
title: "About this website"
linkTitle: "About this website"
weight: 20

---

SAMT-BU Docs is a static documentation website developed as part of the project SAMT-BU (Joined-up services for children and young people). The site is one of several documentation channels in the project and brings together professional content accessible to all project partners. The site collects professional documentation, architecture descriptions, use cases, and guides in one place – accessible to all project partners.

## What you will find here

Content is under development. Here is some of what is being built.

- **Needs and use cases** – a set of numbered use cases describing the key needs that digitalisation is intended to address
- **Architecture and target picture** – capability maps, services, user journeys, and processes
- **Solutions** – technical documentation and guides for those who build and maintain the platform
- **Framework** – methodology, law, governance, standards, and terminology

## Technical platform

The site is built with [Hugo](https://gohugo.io/) (a static site generator) and published via Cloudflare Pages. Content is written in Markdown and version-controlled in Git. Bilingual support (Norwegian and English) is built in.

Content from team repositories is automatically mounted into the site via Hugo Modules, and CMS editing is available directly in the browser via a built-in solution – without any technical knowledge of Git or Markdown.

## Login and access

To edit content, you log in with a GitHub account. SAMT-BU Docs uses a **GitHub App** – not a broad OAuth permission. This means the app only gains access to the specific repositories in the SAMT-X organisation where the app is installed, not to other repositories on your account.

If you submit a suggestion (as a user without write access), a dedicated bot account (`samt-x-bot`) performs the technical GitHub operations on your behalf. Your suggestion is recorded as a pull request with your GitHub username, but the bot handles the actual writing to the repository.

You can revoke access at any time via your GitHub settings (Settings → Applications → Authorized GitHub Apps).

A full risk assessment with details on architecture and compensating controls is available in [Technical documentation → Risk assessment](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/risikovurdering/).

## See also

- [How to Contribute](/samt-bu-docs/om/hvordan-bidra/) – get started with editing and contributions
- [SAMT-BU Docs – solution documentation](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/) – technical documentation and user guide for editors
