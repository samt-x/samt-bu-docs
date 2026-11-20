---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 625201ce-5dd3-4492-be69-e939b0bc6826
title: Fellesløsninger og europeiske krav
weight: 10
---

*Hva må norske fellesløsninger tilpasses for å samvirke med europeiske data spaces og andre europeiske krav? Denne siden er et utkast til diskusjon. Spørsmålene er ikke en liste over mangler, men det vi må finne ut av sammen med dem som eier løsningene.*

Arbeidet følges opp i [samt-bu-architecture#37](https://github.com/samt-x/samt-bu-architecture/issues/37).

---

### Hvorfor dette er viktig

Europeiske data spaces, EUDI-lommeboken og Once-Only bygger på felles standarder og en føderert arkitektur. Hver deltaker kan beholde egne løsninger, så lenge de følger de felles kravene. For norske fellesløsninger er det en mulighet til å bli Norges tilkoblingspunkt, og til å nå lenger ut enn i dag. Forutsetningen er samsvar. Bakgrunnen står under [Relevans for norske aktører](/innsikt/eu-relatert/data-spaces/loesninger/simpl/relevans-for-norge/) i omtalen av Simpl.

De rettslige sidene av kravene hører hjemme under [Juss](/arkitektur/juss/). Her ser vi på løsningene.

---

### Utkast: løsninger som bør analyseres

| Fellesløsning | Må samsvare med | Hvor kravet kommer fra | Spørsmål som må avklares |
|---|---|---|---|
| Altinn Autorisasjon og tilgangsstyring | Bruksvilkår uttrykt i ODRL | Data spaces (DSSC, Simpl) | Kan reglene i Altinn (XACML) oversettes til ODRL, eller trengs det en bro? |
| Samtykke og fullmakt i Altinn | Samtykke og avtaler mellom deltakere i et data space | Data spaces (Simpl-Open 5.0), Data Governance Act | Kan norske samtykker og fullmakter brukes og etterprøves i et europeisk data space? |
| Altinn Studio | Connector og Dataspace Protocol | Data spaces | Kan tjenester bygd med Altinn Studio tilby og hente data som ressurser i et data space? |
| ID-porten og Ansattporten | Verifiserbare attester, OID4VP | eIDAS 2.0 (EUDI-lommeboken), data spaces | Hvordan går overgangen fra innlogging med OIDC til attester fra lommeboken? |
| Maskinporten | Tillit mellom connectorer, maskin til maskin | Data spaces, eIDAS 2.0 (e-segl) | Kan Maskinporten og virksomhetssertifikater brukes, eller trengs attester for virksomheter? |
| Lommeboken og tillitstjenester | Utstedelse og kontroll av attester | eIDAS 2.0 | Hvem utsteder attestene deltakerne i et data space trenger, og hvilke må være kvalifiserte? |
| data.norge.no og Felles begrepskatalog | DCAT-AP, kontrollert vokabular (SKOS) | SEMIC (Interoperable Europe), data spaces | Hvor godt samsvarer DCAT-AP-NO med DCAT-AP, og kan norske begreper gjenbrukes i europeiske vokabularer? |
| Enhetsregisteret og Folkeregisteret | Opplysninger om deltakerne (virksomheter og personer) | Data spaces (innlemming av deltakere), eIDAS 2.0 | Kan registrene være autoritative kilder for attester om deltakerne? |
| KS Fiks | Tilkoblingspunkt for kommunene | Data spaces (blant annet smarte samfunn, mobilitet og energi) | Kan én felles tilkobling dekke alle kommuner, i stedet for én per kommune? |
| eFormidling og meldingsutveksling | Dataoverføring etter Dataspace Protocol, Once-Only (OOTS) | Data spaces, Single Digital Gateway | Blir dette parallelle spor, eller trengs det en bro? |

Lista er et utgangspunkt. Mangler en løsning, eller er et spørsmål feil stilt, si fra i issuet eller med «Gi kommentar» på denne siden.

---

### Norske løsninger med europeisk potensial

Noe av det Norge har bygd, kan også være et bidrag til andre land, ikke bare noe som må tilpasses. Kandidater er Altinn Studio, som verktøy for å lage digitale tjenester, og Designsystemet, som felles grunnlag for brukergrensesnitt i offentlig sektor.

*Vår vurdering:* Dette er en annen problemstilling enn samsvar, og den bør holdes atskilt fra tabellen over. Vi har ikke kartlagt om eller hvor løsningene brukes utenfor Norge.

---

### Neste steg

- Gå gjennom utkastet med produkteierne, én løsning om gangen, og begynn med Altinn Autorisasjon, ID-porten og Maskinporten, lommeboken og data.norge.no.
- Bruke [Simpl-Labs](/innsikt/eu-relatert/data-spaces/loesninger/simpl/simpl-labs/) til å teste de spørsmålene som kan testes.
- Få de rettslige kravene vurdert under [Juss](/arkitektur/juss/).
