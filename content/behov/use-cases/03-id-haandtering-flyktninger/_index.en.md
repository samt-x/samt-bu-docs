---
id: "6d076c0e-d83d-4590-945b-e8695201138e"
title: "3. Handling of D-numbers and Identity Number Changes"
linkTitle: "3. D-number Management"
weight: 30
toc: true
# Valid status values:
# ◍ New
# ◔ Early draft
# ◐ In progress
# ◕ For QA
# ⏺ Approved
# ⨂ Cancelled
status: "Early draft"
last_editor: erikhag1git (Erik Hagen)

---

## Brief description

- Identity management for refugees and asylum seekers
- Change of identity number
- Safeguarding a person's data and rights when their identity number changes

### Who submitted this case?

Bergen Municipality.

## The problem today

Within the childhood and education sector, there is no shared solution for assigning identity numbers to persons who have not yet been assigned a D-number or national identity number (F-number) in the National Population Register. As a rule, parents receive a D-number in connection with tax registration, whereas it may take considerably longer before children receive a D-number or national identity number. In the meantime, municipalities must register a number of fictitious identity numbers in accordance with their own internal arrangements. Person objects therefore potentially arise with a range of different identifiers across the public sector.

### Where do breakdowns in information flow or responsibility occur?

Municipalities provide services to persons who are not yet registered with a D-number or national identity number (F-number) in the National Population Register. Municipalities are therefore compelled, within their respective sectors, to create one or more fictitious versions of these person objects while awaiting the assignment of an identity number in the National Population Register. There is no coordination of such fictitious numbers between sectors or between different municipalities and county authorities.

## Actors

### Affected actors

- Parents who lose access or lose data
- Children and pupils who lose data

## Consequences of the current situation

Municipalities have a duty to provide persons with certain services, such as a place in a nursery or a school place, even when those persons do not have an identity number in the National Population Register.

When persons subsequently receive an identity number in the National Population Register, there is no automatic mechanism by which the municipality can say with certainty that new person objects imported from the register are, with 100% confidence, the same as those the municipality has registered in its various systems using a fictitious number. Only a match in name and address can provide some degree of indication of this. In the worst case, errors can occur. The situation is somewhat simpler when a child subsequently receives a D-number or national identity number, as the parental relationships are generally included in the data flow from the National Population Register at that point. Unfortunately, this often occurs long after the parents have received such a number in the register.

Many systems support the transition from a D-number to a national identity number (F-number) by means of an integration that communicates the change. This enables an automated transition, which in turn potentially ensures that data is not lost or made inaccessible.

The identity number is generally the primary key for person objects. Without automation or robust controls, duplicate person objects will therefore typically arise in multiple systems. This can result in information not being found – such as decisions – or in parents or pupils losing data they have stored in various IT systems.

Fictitious numbers also do not provide access to log in to public IT systems via ID-porten.

The health sector has progressed further towards a shared solution in this area, as we understand it, with something called a Help Number (Hjelpenummer). More about this can be read here, along with the challenges described, which are well comparable to those in other public sectors:
https://www.nrk.no/norge/darlig-id-system-en-pasientfare-1.11425318

## Desired situation

It becomes possible to create identities in the National Population Register, or in the FIKS population register, which becomes a shared solution across all sectors. Some automation is built in to prevent municipalities from creating duplicates, such as checks against name, date of birth, and home address. It is possible to register the same data as for persons with a national identity number, such as parent–child relationships. Parental responsibility is set as unknown.

This identity is established as a fully valid member of the identity management system and provides access to ID-porten. Upon transition to a D-number or national identity number, the system ensures that the fictitious number (referred to as an H-number, as in the health sector) is replaced and notified through integrations so that other systems can carry out a controlled and automated transition to the new number. Since the health sector already has such a system, it would be advantageous if this new system could retrieve the H-number with data from the health sector in order to avoid duplicate H-numbers across the health sector and other sectors.

## Insight work

Simpler user journeys for staff, parents and guardians, pupils, and students throughout the educational pathway – from nursery to primary school, upper secondary education, and higher education.

## Project objectives addressed

- Shared information models and standardised interfaces that over time cover "all" areas and sectors.
- Scaling and transfer of the project's learning and outputs to other areas and sectors, following piloting in this project.
