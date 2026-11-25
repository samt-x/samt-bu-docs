---
# id: auto-generated – copied values are overwritten automatically on push
id: 625201ce-5dd3-4492-be69-e939b0bc6826
title: Shared solutions and European requirements
weight: 10
---

*What must Norwegian shared national solutions adapt to work together with European data spaces and other European requirements? This page is a draft for discussion. The questions are not a list of shortcomings, but what we need to find out together with those who own the solutions.*

The work is followed up in [samt-bu-architecture#37](https://github.com/samt-x/samt-bu-architecture/issues/37).

---

### Why this matters

European data spaces, the EUDI wallet and Once-Only build on common standards and a federated architecture. Each participant can keep its own solutions, as long as they follow the common requirements. For Norwegian shared national solutions, this is an opportunity to become Norway's connection point, and to reach further than today. The precondition is compliance. The background is described under [Relevance for Norwegian digital infrastructure](/en/innsikt/eu-relatert/data-spaces/loesninger/simpl/relevans-for-norge/) in the section on Simpl.

The legal aspects of the requirements belong under [Legal](/en/arkitektur/juss/). Here we look at the solutions.

---

### Draft: solutions that should be analysed

| Shared solution | Must comply with | Where the requirement comes from | Questions to be clarified |
|---|---|---|---|
| Altinn Authorisation and access management | Usage terms expressed in ODRL | Data spaces (DSSC, Simpl) | Can the rules in Altinn (XACML) be translated to ODRL, or is a bridge needed? |
| Consent and power of attorney in Altinn | Consent and agreements between participants in a data space | Data spaces (Simpl-Open 5.0), Data Governance Act | Can Norwegian consents and powers of attorney be used and verified in a European data space? |
| Altinn Studio | Connector and Dataspace Protocol | Data spaces | Can services built with Altinn Studio offer and retrieve data as resources in a data space? |
| ID-porten and Ansattporten | Verifiable credentials, OID4VP | eIDAS 2.0 (EUDI wallet), data spaces | How does the transition from login with OIDC to credentials from the wallet work? |
| Maskinporten | Trust between connectors, machine to machine | Data spaces, eIDAS 2.0 (e-seals) | Can Maskinporten and enterprise certificates be used, or are credentials for organisations needed? |
| The wallet and trust services | Issuing and verifying credentials | eIDAS 2.0 | Who issues the credentials that participants in a data space need, and which must be qualified? |
| data.norge.no and the national concept catalogue | DCAT-AP, controlled vocabulary (SKOS) | SEMIC (Interoperable Europe), data spaces | How well does DCAT-AP-NO align with DCAT-AP, and can Norwegian concepts be reused in European vocabularies? |
| The Central Coordinating Register for Legal Entities and the National Population Register | Information about participants (organisations and persons) | Data spaces (onboarding of participants), eIDAS 2.0 | Can the registers be authoritative sources for credentials about participants? |
| KS Fiks | Connection point for municipalities | Data spaces (including smart communities, mobility and energy) | Can one common connection cover all municipalities, instead of one per municipality? |
| eFormidling and message exchange | Data transfer according to the Dataspace Protocol, Once-Only (OOTS) | Data spaces, Single Digital Gateway | Will these be parallel tracks, or is a bridge needed? |

The list is a starting point. If a solution is missing, or a question is wrongly put, say so in the issue or with "Give feedback" on this page.

---

### Norwegian solutions with European potential

Some of what Norway has built may also be a contribution to other countries, not just something that must be adapted. Candidates are Altinn Studio, as a tool for building digital services, and Designsystemet, the Norwegian design system, as a common basis for user interfaces in the public sector.

*Assessment:* This is a different question from compliance, and it should be kept separate from the table above. We have not mapped whether or where these solutions are used outside Norway.

---

### Next steps

- Go through the draft with the product owners, one solution at a time, starting with Altinn Authorisation, ID-porten and Maskinporten, the wallet and data.norge.no.
- Use [Simpl-Labs](/en/innsikt/eu-relatert/data-spaces/loesninger/simpl/simpl-labs/) to test the questions that can be tested.
- Have the legal requirements assessed under [Legal](/en/arkitektur/juss/).
