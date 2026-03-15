---
id: e0d42db3-b997-4bcc-9bf5-4da622c18429
title: "22. Analysis Data from Kindergarten to Adult Education"
linkTitle: "22. Analysis data across the full pathway"
weight: 220
toc: true
status: "Early draft"
# Valid status values: New | Early draft | In progress | For QA | Approved | Cancelled
last_editor: erikhag1git (Erik Hagen)

---

## Brief Description

There is a need for data from the entire education sector that can say something about «how things turned out» for different pupils – from kindergarten to adult education. Data is used at an aggregate level but must be based on individual data.

Vestland County Municipality has established a solution for analysing data from sources including VIGO, which they share with the municipalities in the county. This case builds on what Vestland FK has already achieved and points to the need to extend this to cover the full educational pathway – and make equivalent solutions available to more actors.

### Who submitted this case?

Vestland FK (Vestland County Municipality).

## The Problem Today

Social background, results and effort are interconnected throughout the entire educational pathway – from kindergarten to higher education and working life. To understand the full picture and intervene where «problems arise», data covering the full pathway at individual level (aggregated for analysis) is needed. Today, this does not exist.

### Where do breaks in information flow or responsibility occur?

Breaks occur particularly:

* between kindergarten and primary school – different systems, different owners, no shared data flow
* between primary school and upper secondary – municipal and county responsibility divides here
* between upper secondary and higher education – county and state responsibility
* between education and working life – very limited connection

## Actors

### End users (of analysis data)

* Municipalities – to assess the effect of interventions and plan resource use
* County municipalities – to follow student flow and educational outcomes over time
* Political leadership at various levels – for evidence-based decision-making
* Children, young people and guardians – indirectly, through better adapted services

### Service staff

* Analysts and planners in municipalities and county municipalities
* School leadership and advisors

### System vendors

* Vendors of kindergarten and school administration systems (VIGO, IST, Visma, etc.)
* Vendors of analytics platforms and data sharing services

### Stakeholders

#### Directorates

* **Utdanningsdirektoratet** – professional directorate for primary and secondary education; manages central educational data
* **Statistics Norway (SSB)** – manages population and education statistics at individual level
* **Digitaliseringsdirektoratet** – cross-sectoral stakeholder for data sharing and interaction

#### Ministries

* **Ministry of Education and Research** – overall responsibility for the education sector
* **Ministry of Digitalisation and Public Administration** – overall responsibility for data sharing and cross-sectoral initiatives

### Service providers

* **Municipalities** – own and manage data from kindergarten and primary school
* **County municipalities** – own and manage data from upper secondary education

### Coordinating and supporting actors

* **KS and KS Digital** – coordinate the municipal sector and deliver shared digital solutions
* **Sikt** – delivers and manages shared services in the education sector

## Consequences of the Current Situation

### For end users (municipalities, county municipalities and political leadership)

* Poor overview of the connections between different phases of life
* Difficult to identify patterns and assess the effect of interventions across education levels
* Decisions must be made on a weaker evidence base than necessary

### For service staff

* Analyses must be built manually across systems without shared infrastructure
* Much time is spent on data collection and consolidation rather than analysis

### For organisations

* Inefficient use of resources – the same work is done in parallel across many municipalities and county municipalities
* Harder to collaborate on shared insights across municipalities and levels of government

### At system level

Without data covering the full educational pathway, it is difficult to measure the effect of long-term interventions, identify risk groups early enough, or plan targeted support for an entire population cohort from kindergarten to working life.

## Desired Situation

In a desired situation, municipalities and county municipalities can easily access coherent data from kindergarten, primary school, upper secondary and beyond – at an aggregate level that respects privacy, but based on individual data. This provides a real basis for assessing the effect of interventions over time, identifying patterns across education levels and planning resource use in a targeted way.

Analytical capacity that today exists only in well-resourced county municipalities (such as Vestland FK) should be made available to all municipalities – regardless of size or their own technical resources.

## Input on Solution Choices

### Vestland FK's existing solution as a starting point

Vestland FK has established a solution in which data from sources including VIGO is analysed and shared with municipalities in the county. One example is the student flow in upper secondary education, where year by year one can see the status for students: who starts what, how many progress, who makes alternative choices, who drops out, and final competence outcomes. This can be filtered by sending municipality, sending lower secondary school, lower secondary grades, absence levels, gender, etc.

In an extended solution, equivalent data from kindergarten and primary school could be placed to the left of this picture, and higher education/employment status to the right – making the entire life course visible in one coherent analysis.

![Example of student flow in upper secondary education in Vestland FK](elevflyt-vestland.png)

### Shared municipal data platform – KS Digital / Azure Databricks

KS Digital is working on a shared municipal data platform based on Azure Databricks. Such a platform could give municipalities and county municipalities access to a shared infrastructure for storing, processing and analysing data across services and sectors – without each municipality having to build and operate this independently.

> **⚠ Note:** The details of KS Digital's specific plans, progress and scope for this platform have not been verified in this document. This section should be updated with references to official sources and clarification of what is planned versus decided.

If such a platform is realised, it would be a natural foundation for this case on analysis data across the full pathway – allowing data from kindergarten, primary school, upper secondary and beyond to be consolidated in a shared infrastructure with common access control and privacy mechanisms.

## Insight Work

The case builds on input from Vestland FK, which has practical experience with analysing VIGO data shared with municipalities. These experiences are relevant as a model for what is possible, and what data infrastructure and agreements are required.

## Relevant Project Goals

* Common information models and standardised interfaces that over time cover «all» areas and sectors
* Reusable and shared solutions – analytical capacity available to all municipalities
* Simpler user journeys for employees, guardians, students and pupils throughout the learning pathway
* Collaboration and innovation across public actors in the ecosystem
* Long-term goals of lifelong learning
* Scaling and transfer of the project's learning and products to other areas and sectors
