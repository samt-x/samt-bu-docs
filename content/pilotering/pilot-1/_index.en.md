---
# id: auto-generated – copied values are overwritten automatically on push
id: "43b084cb-6951-4529-86f4-3d56f939a51e"
title: "Pilot 1 – architecture"
linkTitle: "Pilot 1 – architecture"
weight: 20

---

*Working document – Architecture and target picture, SAMT-BU*

## Purpose

This document describes a proposed overall architecture, POC/MVP architecture and work items related to SAMT-BU. The document builds on work carried out in sprint 1.

## Tasks in sprints 1–3

- Select architecture for MVP/POC and document it
- Treat the architecture as a plan that may change as we learn
- Assess reuse of existing common solutions, methods and frameworks – and justify choices
- Evaluate multiple architecture alternatives
- Ensure the architecture aligns with the dream journey
- Define overall architecture (much of this will come in later phases, particularly regarding the information model)
- Define architecture for MVP/POC

The main goal of sprint 1 is to select an architecture for the MVP and document it.

## Overall architecture

Most of this is based on notes from our meetings.

Architecture choices shall be evaluated against clear principles:

- **Reusability:** The solution must be usable by multiple sectors (municipal, county and state) without major adaptations.
- **Pattern-based design:** We will use established integration and data flow patterns.
- **Openness and flexibility:** The architecture must allow alternative implementations and gradual extension.
- The architecture must make data ready for future needs (e.g. AI analysis of dropout, cross-sectoral collaboration with health, budget planning).
- **Pilot-based learning:** Before the final architecture is decided, the principles shall be tested in a POC with real data.

### Common information model

A common information model is necessary for data flow between primary school, county and other services. Topics we have discussed include centralised vs. distributed models, ownership, access control and integration with national data catalogues.

Questions we need to work through:

- We start with FINT. Are there other information models we should also lean on?
- Do we start with, for example, person? Resident?
- Should we work on defining ontologies? Do we have something to build on?
- Can we start small and instead develop data contracts with individual municipalities? With a decentralised model this would make sense.

### Governance and security

Governance and security are absolutely central to SAMT-BU. The following requirements must be met:

- documented access control (logical and organisational)
- traceability of who gains access to which data
- isolation between county authorities (this must also be considered in relation to NAIS and FLØIS patterns)
- assessment of ROS and DPIA – particularly regarding storage, deletion and further processing of pupil data

### Data flow

The data flow in SAMT-BU shall be transparent and fully traceable. A POC or MVP calls for simple synchronisation between services and clear API interfaces. Further work must be considered alongside the dream journey work in the other working group.

## Proposed architecture for Proof of Concept

The working group has discussed MVP vs. POC. We recommend the latter in order to get started quickly and demonstrate how we can solve the actual problem while illustrating the potential for further data use.

The goals of a POC are as follows:

- The POC shall demonstrate actual data flow between primary school and upper secondary.
- Focus shall be on functionality and learning, not a 100 % finished solution.
- Testing of the information model (FINT), integrations and access control.

The following principles will underpin the POC architecture:

- Modular architecture with clearly bounded domains.
- Simple integration with existing common components (e.g. FIKS, authorisation).
- Data flow that supports sharing, quality assurance and traceability.
- Ability for stepwise extension based on learning in the project.
- The specialist systems (Visma/Vigilo) are the primary source for data capture and case handling.
- SAMT-BU shall only retrieve and make available data with documented value.

The proposed architecture shall provide a flexible and robust platform for SAMT-BU, with particular emphasis on reuse of existing technologies and a clear separation between domains.

So far we have discussed two architecture alternatives: KS Digital's solution for common data management, or integration between the municipalities' SAS and FINT. This is an ongoing initiative linked to a common service platform, aiming to facilitate:

- a structured and coordinated way of managing data across actors and systems
- support for standardisation, sharing and reuse of data, information models and infrastructure
- support for different data needs in the municipal sector (production/development, consumption/use and knowledge sharing)
- a basis for data-driven services, better decisions and artificial intelligence

### Alternative 1: Centralised integration and data platform through KS Digital

The advantage of using this solution is that the infrastructure is already in place, allowing us to get started quickly with an MVP and/or POC. In addition, we will cover the need for data sharing and reuse across the sector – not only within children and education, but also into other areas such as health and care, planning/building/technical, social welfare etc.

*Architecture sketches: Should we include the sketches reviewed in the working group, or wait until clarification around POC/MVP?*

### Alternative 2: Decentralised integration between FINT, municipal SAS, Vigo Skole and others

*(Detailed exchange – to be filled in)*

## Target picture and the road ahead

The long-term target picture builds on scaling the POC into a full solution for SAMT-BU.

Proposals for sprints 2 and 3:

- Establish a foundation for data-driven service development
- Establish technical architecture: Set up end-to-end data flow (from source to recipient) in the platform.
- Prove source independence: Demonstrate that the architecture handles data from different sources (both Vigilo and Visma) and maps them to the same structure.
- Legal framework: Complete necessary clarifications (ROS) related to data sharing and privacy across administrative levels.
- Semantics and data-centric core:
  - Information modelling: Define and publish the core objects «Person v1.0» and «Pupil relationship v1.0» in a common information model (independent of specialist system). We must think holistically from primary school to higher education from day one.
  - Data contracts: Establish machine-readable contracts as the governing interface between data producer (primary school) and data consumer (upper secondary/county).
  - Semantic validation: Test and verify that the concepts in the contract are understood equally by both sender and receiver (avoiding misunderstandings about e.g. «absence»).
- Data management and value creation:
  - The data product «School leaver» (to be discussed further – a proposal only): Make relevant data available via API/sharing to upper secondary for enrolment and planning.
  - Process support: Verify that the recipient (upper secondary) can use the data directly in their processes without manual cleansing or conversion.
  - Analysis basis: Make aggregated data available for reporting and governance.
  - Data basis for AI: Make data available for AI models that can identify patterns and support early intervention and better resource management.
  - Problem solving: Verify that we actually solve the core problem: transferring information from primary school to upper secondary in a way that provides a basis for joined-up services.

## Other tasks

- Archiving tasks?

## Dependencies

- The user journey: SAMT-BU: Transfer of pupils – Miro
- The supplier market: We should also write something here, particularly regarding standardisation etc.
