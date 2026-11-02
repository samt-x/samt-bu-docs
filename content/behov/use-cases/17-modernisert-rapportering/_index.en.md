---
# id: auto-generated – copied values are overwritten automatically on push
id: "f3c85e96-d5c9-4cd7-b29b-f05bda058448"
title: "17. Modernised Reporting from Municipalities to the State"
linkTitle: "17. Modernised Reporting"
weight: 250
toc: true
# Valid status values:
# ◍ New
# ◔ Early draft
# ◐ In progress
# ◕ For QA
# ⏺ Approved
# ⨂ Cancelled
status: Early draft

---
## 1. Goal

The goal is to ensure that state authorities receive the management data they need from the local government sector with a minimal administrative burden. By shifting the focus from many different manual extracts to data sharing within a modern architecture, we aim to ensure high data quality for national statistics, while also making the data available for municipal management, data-driven innovation and coherent services for children and young people.

## 2. Actors

- **Caseworker in the municipality:** Registers data as a natural part of the professional follow-up.
- **Line-of-business system (municipality):** The source system that acts as "master" for the data and publishes messages about changes.
- **State recipient (SSB/directorate):** Consumer of data that needs insight for statistics, analysis and control.
- **Integration platform (shared solution):** Conveys event messages and handles access control for API lookups.

## 3. Preconditions

- **Standardisation:** Shared information models and code lists are in place for the service areas concerned.
- **Authorisation:** Use of Maskinporten for secure authentication between the systems.
- **API readiness:** The line-of-business systems must be able to expose standardised interfaces for data sharing.

## 4. Trigger

A relevant event occurs in the municipal line-of-business system that is significant for national reporting (e.g. a decision made, an investigation concluded or a service changed).

## 5. Main flow (the modern data flow)

1. **Event occurs:** A caseworker completes a registration in the line-of-business system.
2. **Local validation:** The line-of-business system immediately checks the data against built-in KOSTRA rules (KOSTRA: municipal–state reporting), so that any gaps are corrected straight away.
3. **Event publication (Track A):** The line-of-business system sends a lightweight message (notification) to a central message queue. The message contains only metadata (what happened and a unique reference ID), not sensitive details.
4. **Data retrieval via API (Track B):** The state recipient picks up the notification and makes an automated API lookup against the municipality's line-of-business system to retrieve the specific details it has a legal basis to see. Notifications can be event-driven or state-driven (e.g. register quality achieved, or reporting deadline passed).
5. **Receipt and log:** The system logs that data has been disclosed, and the municipality receives confirmation that the reporting obligation for this event has been fulfilled.

## 6. Alternative flows

- **6a. Modernised submission (Track C):** For areas where API lookups are not yet supported, the line-of-business system packages the data and sends it automatically as a completed message to the state's receiving point (e.g. via Altinn), with no manual work for the caseworker.
- **6b. Handling of deviations:** If the state discovers logical errors in the retrieved data, a digital alert is sent back to the municipality's line-of-business system for correction at the source.

## 7. Benefits

- **Administrative savings:** Removes the need for heavy reporting periods at year end; reporting happens "by itself" throughout the year.
- **Better data quality:** Validation takes place while the case is fresh, which reduces errors and rework.
- **Security and privacy:** By sending notifications first and retrieving data afterwards (Track A+B), the amount of sensitive information "flowing" unnecessarily between systems is minimised.
- **Capacity for innovation:** Structured data becomes available for the municipality's own analyses in real time, not just for state statistics a year later.

## 8. Input to solution choices

The choice of technical implementation must balance the municipality's need for simplification against the state's (e.g. SSB's) need for stability and handling of volume.

- **Recommended solution: Hybrid event-driven API model (Track A+B)**:This pattern (Notification-first) is the most future-oriented. It ensures that the state always has access to the latest data without the municipality having to push large amounts of sensitive files out of the organisation. It also supports "coherent services", since other authorised actors can subscribe to the same events.

- **Transitional solution: Automated submission (Track C)**:To ensure progress, a model should be supported where the line-of-business systems can "push" data directly to state receiving points. This requires less change in state IT architectures in the short term, but should be seen as a step on the way to full API-based sharing.

## 9. Need for further work

- **Dialogue with SSB:** Clarify their roadmap for receiving data and their willingness to move from "file reception" to API lookups.
- **Information modelling:** Continue the work on a shared selection of concepts so that an "event" means the same thing in all systems.
- **Piloting:** Test Track A+B in a limited field within child welfare or health services to document the actual reduction in time spent.
