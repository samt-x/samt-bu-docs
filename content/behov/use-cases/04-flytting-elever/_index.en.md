---
# id: auto-generated – copied values are overwritten automatically on push
id: "105fab2b-19bb-47e2-a292-44cd50cbf7d6"
title: "4. Relocation of Pupils Between Municipalities/County Authorities During the School Year"
linkTitle: "4. Pupil Relocation"
weight: 120
toc: true
# Valid status values:
# ◍ New
# ◔ Early draft
# ◐ In progress
# ◕ For QA
# ⏺ Approved
# ⨂ Cancelled
status: In progress

---
## 1. Goal

The goal is to ensure that necessary information about a pupil follows the pupil digitally and automatically when they move between municipalities and county authorities during the school year. This is to ensure continuity in education, especially for vulnerable children, and to reduce the time from moving in until the child receives adapted provision at the new school.

## 2. Actors

- **Pupil/Parents:** Move and register the move with the new municipality/county authority.
- **School administration (municipality/county being left):** Responsible for ending the pupil's enrolment and making documentation available.
- **School leader/Teacher (receiving municipality/county):** Receives the pupil and needs quick insight into the pupil's history and needs.
- **Line-of-business systems (e.g. Vigilo, Visma Flyt Skole, IST):** The systems that are to exchange the data.
- **The National Population Register (Folkeregisteret, FREG):** The source that triggers the relocation event.

## 3. Preconditions

- The pupil is registered as having moved in the National Population Register, or the parents have accepted a school place in the new municipality/county.
- There is a legal basis for sharing confidential information (or consent from parents where required).
- Shared standards for exchanging pupil records (e.g. according to SIKT or KS standards).

## 4. Trigger

A relocation event is registered, either when parents apply for a school place in a new municipality, or via an automatic notification from the National Population Register about a change of address.

## 5. Main flow (the modern data flow)

1. **Relocation notice:** The receiving municipality's line-of-business system receives a notification that a new pupil is moving to the municipality.
2. **Event notification (Track A):** The receiving municipality sends a request (via a shared core) to the municipality being left for access to the pupil's digital record.
3. **Automatic check and authorisation:** The system of the municipality being left verifies identity and the legal basis for sharing.
4. **Data retrieval via API (Track B):** The receiving municipality retrieves the necessary "basic package" (grades, absence, group membership) and any "extended package" (IEP, expert assessments) directly from the source system in the municipality being left.
5. **Preparation:** The teacher at the new school receives an alert in their line-of-business system: "New pupil starts Monday – documentation is ready for review."

## 6. Alternative flows

- **6a. Need for consent:** If the data is of such a nature that consent is required, a message is triggered to the parents in a citizen portal for digital signing before the data is released.
- **6b. Lack of digital maturity:** If the municipality being left does not have API support, a standardised export file (Track C) is generated and sent via secure digital mail to the new school.

## 7. Benefits

- **The best interests of the child:** The pupil experiences a safer transition without "gaps" in follow-up.
- **Resource savings:** Teachers no longer have to spend weeks chasing documentation and assessing the pupil again from scratch.
- **Data quality:** The information is correct and up to date, not based on oral handovers or outdated paper copies.

## 8. Input to solution choices

For this to work nationally, we must avoid every municipality building its own integrations with all the others.

- **Recommended solution: Hybrid event-driven API model (Track A+B)**:We should use an architecture where the relocation acts as an *event* that triggers a rights-controlled *retrieval* of data. By using "Notification-first", we can ensure that sensitive data is only moved when there is a confirmed need at the recipient.
- **Standardised pupil record:** It is critical that the content of the digital "removal load" is standardised (semantic interoperability). Moving the data is of little help if core concepts are defined differently in the two systems.

## 9. Need for further work

- **Legal clarification:** Ensure that the General Data Protection Regulation (GDPR) is complied with in the automatic transfer of sensitive pupil data between municipalities.
- **Supplier dialogue:** Coordinate with the major school system suppliers to ensure they implement the same API standards.
- **Link to child welfare/PPT:** Investigate whether the relocation event should also trigger a similarly seamless transfer in other sectors for children with complex needs.
