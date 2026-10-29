---
# id: auto-generated – copied values are overwritten automatically on push
id: 5c5afb34-e520-461e-813b-5de086478937
title: "Tasks and follow-up"
linkTitle: "Tasks and follow-up"
weight: 25
---

This page has the links you need to follow up the work in SAMT-BU: your own tasks, the boards of the sub-projects, and the portfolio for the whole project. The tasks and boards live in GitHub and are open to everyone. Only the searches for your own tasks require you to be signed in, because GitHub needs to know who you are.

How task management is set up, and the rules we follow, are described under [Task management](https://docs.samt-bu.no/en/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/).

Use the links on this page to find your way. The list of all boards in GitHub, under Projects in the organisation, also shows the overview boards. They are called «SAMT-BU Overview – …» and are not sub-projects.

## New task or input

Go to the repository where the issue belongs, choose **Issues** and **New issue**, and pick the form for the kind of issue: task, solution proposal, question, decision, risk or problem. The forms are the same in all repositories, and are in Norwegian. Where the issue belongs, and how to fill in the form, is described in the [User guide for task management](https://docs.samt-bu.no/en/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/brukerveiledning/).

## My tasks

Ready-made searches across all repositories and boards in SAMT-BU. Consider bookmarking them. Both require you to be signed in to GitHub.

| Search | Shows |
|---|---|
| [My open tasks](https://github.com/issues?q=is%3Aissue%20is%3Aopen%20assignee%3A%40me%20org%3Asamt-x) | Open tasks assigned to you (Assignee) |
| [Tasks mentioning me](https://github.com/issues?q=is%3Aissue%20is%3Aopen%20mentions%3A%40me%20org%3Asamt-x) | Open tasks where someone has mentioned you with @ |

The searches only list tasks where you are an **Assignee** or are mentioned. That is why assigning tasks matters.

If you are **responsible** for tasks in the architecture group, you can see them in the view [By responsible](https://github.com/orgs/samt-x/projects/5/views/3) in Project 5. Across all boards, you find your responsibilities on the aggregate board, see below. GitHub's search does not see the fields on the boards.

## Tasks that need follow-up

| Search | Shows |
|---|---|
| [Open tasks assigned to nobody](https://github.com/search?q=is%3Aissue%20is%3Aopen%20no%3Aassignee%20org%3Asamt-x&type=issues) | Tasks without an Assignee, which may fall between the cracks. Works without signing in. |
| [Blocked tasks](https://github.com/search?q=is%3Aissue%20is%3Aopen%20label%3Ablocked%20org%3Asamt-x&type=issues) | Open tasks with the label blocked, waiting for something outside the task. What they are waiting for is stated in a comment. Works without signing in. |

## All tasks in one place

[SAMT-BU Overview – All tasks](https://github.com/orgs/samt-x/projects/12) collects all tasks in the public repositories on one board, with a shared status: Not started, In progress or Done. The board is filled automatically every hour from the project boards, and also shows the responsible person, priority and dates from there.

Change tasks on the project board they belong to. Changes made on the aggregate board are overwritten on the next update.

| View | Shows |
|---|---|
| [My tasks](https://github.com/orgs/samt-x/projects/12/views/1) | Your open tasks, as a kanban by status (requires sign-in) |
| [By responsible](https://github.com/orgs/samt-x/projects/12/views/2) | Open tasks, one column per responsible person |
| [By board](https://github.com/orgs/samt-x/projects/12/views/3) | Open tasks, grouped by repository |
| [Blocked](https://github.com/orgs/samt-x/projects/12/views/4) | Open tasks with the label blocked |
| [Timeline](https://github.com/orgs/samt-x/projects/12/views/5) | Open tasks along a timeline |

## The project boards

A **project board** is a project in GitHub (GitHub Projects): a collection of tasks with shared fields, such as status, owner and deadline. The same board can be shown in several ways, and each view has its own tab on the board:

- **Kanban board** (in GitHub: Board): one column per step in the workflow, for example New, In progress and Done. Each task is a card that moves from left to right as the work progresses. The columns can also be based on another field, for example owner or priority.
- **Table**: one row per task, with the fields as columns. Useful for sorting and filtering.
- **Timeline** (Roadmap): the tasks placed along a time axis by date.

Moving a card to another column changes the field the columns are based on, usually status. The change shows in all views, because it is the same task.

Each sub-project has its own project board, with its own statuses and fields.

| Sub-project | Board |
|---|---|
| Pilot 1 – Transition from lower to upper secondary school | [Project 1](https://github.com/orgs/samt-x/projects/1) |
| Pilot 2 – Choice of educational path | [Project 2](https://github.com/orgs/samt-x/projects/2) |
| Pilot 3 – Children and young people moving during the school year | [Project 4](https://github.com/orgs/samt-x/projects/4) |
| Pilot 4 – Diplomas | [Project 3](https://github.com/orgs/samt-x/projects/3) |
| Pilot 5 – IDs in education | [Project 9](https://github.com/orgs/samt-x/projects/9) |
| Pilot 6 – Parents' access to data | [Project 10](https://github.com/orgs/samt-x/projects/10) |
| Pilot 7 – Digital dialogue between kindergarten/school and home | [Project 19](https://github.com/orgs/samt-x/projects/19) |
| Framework and generic architecture (the architecture group) | [Project 5](https://github.com/orgs/samt-x/projects/5), with the views [By responsible](https://github.com/orgs/samt-x/projects/5/views/3) and [My tasks](https://github.com/orgs/samt-x/projects/5/views/7) (requires sign-in) |
| Information models | [Project 6](https://github.com/orgs/samt-x/projects/6) |

The boards are based on two shared templates, and all their statuses can be reported at the shared level on the aggregate board. See [Conventions](https://docs.samt-bu.no/en/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/konvensjoner/).

## The SAMT-BU portfolio

The portfolio gives an overview of the whole project, with one card per pilot, product and work area: who owns it, what phase it is in, and how it is going. The portfolio board is [SAMT-BU Overview – Portfolio](https://github.com/orgs/samt-x/projects/13).

| Field | Meaning |
|---|---|
| Status | The phase: Idea, Exploring, In progress, Paused or Done |
| Category | Pilot, Product or Work area |
| Owner | Who owns the card |
| Health | On track, At risk or Off track |
| Target date | When it is due to finish, or the next important date |

The hypothesis and MVP are in the description of each card. The cards are issues in the repository [samt-bu-portfolio](https://github.com/samt-x/samt-bu-portfolio).

Owner, health and dates have not been filled in yet. The governance itself will be described here once the project management has decided on it: what is in the portfolio, who owns what, and how often the portfolio is reviewed.
