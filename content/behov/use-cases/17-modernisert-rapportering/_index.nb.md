---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: "f3c85e96-d5c9-4cd7-b29b-f05bda058448"
title: 17. Modernisert rapportering kommune-stat
linkTitle: 17. Modernisert rapportering
weight: 170
toc: true
# Gyldige statusverdier:
# ◍ Ny
# ◔ Tidlig utkast
# ◐ Pågår
# ◕ Til QA
# ⏺ Godkjent
# ⨂ Avbrutt
status: Tidlig utkast

---
## 1. Mål

Målet er å sikre at statlige myndigheter får nødvendige styringsdata fra kommunesektoren med minimal administrativ byrde. Ved å flytte fokus fra mange ulike manuelle uttrekk til datadeling innenfor en moderne arkitektur, skal vi sikre høy datakvalitet for nasjonal statistikk, samtidig som dataene gjøres tilgjengelige for kommunal styring, datadrevet innovasjon og sammenhengende tjenester for barn og unge.

## 2. Aktører

- **Saksbehandler i kommunen:** Registrerer data som en naturlig del av den faglige oppfølgingen.
- **Fagsystem (Kommune):** Kildesystemet som fungerer som "Master" for dataene og publiserer meldinger om endringer.
- **Statlig mottaker (SSB/Direktorat):** Konsument av data som har behov for innsikt til statistikk, analyse og kontroll.
- **Integrasjonsplattform (Fellesløsning):** Formidler av hendelsesmeldinger og tilgangsstyring for API-oppslag.

## 3. Forutsetninger

- **Standardisering:** Felles informasjonsmodeller og kodeverk er på plass for de aktuelle tjenesteområdene.
- **Autorisasjon:** Bruk av Maskinporten for sikker autentisering mellom systemene.
- **API-beredskap:** Fagsystemene må kunne eksponere standardiserte grensesnitt for datadeling.

## 4. Trigger

En relevant hendelse inntreffer i det kommunale fagsystemet som har betydning for nasjonal rapportering (f.eks. et vedtak fattet, en undersøkelse avsluttet eller en tjeneste endret).

## 5. Hovedforløp (Den moderne datastrømmen)

1. **Hendelse oppstår:** En saksbehandler ferdigstiller en registrering i fagsystemet.
2. **Lokal validering:** Fagsystemet sjekker dataene mot innebygde KOSTRA-regler umiddelbart, slik at eventuelle mangler rettes med en gang.
3. **Hendelsespublisering (Spor A):** Fagsystemet sender en lettvektsmelding (notifikasjon) til en sentral meldingskø. Meldingen inneholder kun metadata (hva som skjedde og en unik referanse-ID), ikke sensitive detaljer.
4. **Datahenting via API (Spor B):** Den statlige mottakeren plukker opp notifikasjonen og gjør et automatisert API-oppslag mot kommunens fagsystem for å hente de spesifikke detaljene de har hjemmel til å se. Notifikasjoner kan være hendelsesdrevne, eller tilstandsdrevne (f.eks oppnådd registerkvalitet, eller passert rapporteringstidspunkt).
5. **Kvittering og logg:** Systemet logger at data er utlevert, og kommunen får en bekreftelse på at rapporteringsplikten for denne hendelsen er oppfylt.

## 6. Alternative forløp

- **6a. Modernisert innsending (Spor C):** For områder der API-oppslag ennå ikke er støttet, pakker fagsystemet dataene og sender dem automatisk som en ferdig utfylt melding til statens mottakspunkt (f.eks. via Altinn), uten manuelt arbeid for saksbehandler.
- **6b. Avvikshåndtering:** Dersom staten oppdager logiske feil i de hentede dataene, sendes et digitalt varsel tilbake til kommunens fagsystem for korrigering ved kilden.

## 7. Gevinster

- **Administrative besparelser:** Fjerner behovet for tunge rapporteringsperioder ved årsslutt; rapporteringen skjer "av seg selv" gjennom året.
- **Bedre datakvalitet:** Validering skjer når saken er fersk, noe som reduserer feil og etterarbeid.
- **Sikkerhet og personvern:** Ved å sende notifikasjoner først og hente data etterpå (Spor A+B), minimeres mengden sensitiv informasjon som "flyter" unødvendig mellom systemer.
- **Innovasjonskraft:** Strukturerte data blir tilgjengelige for kommunens egne analyser i sanntid, ikke bare for statlig statistikk ett år senere.

## 8. Innspill til løsningsvalg

Valg av teknisk realisering må balansere kommunens behov for forenkling mot statens (f.eks. SSBs) behov for stabilitet og volumhåndtering.

- **Anbefalt løsning: Hybrid Hendelsesdrevet API-modell (Spor A+B)**:Dette mønsteret (Notification-first) er mest fremtidsrettet. Det sikrer at staten alltid har tilgang til de nyeste dataene uten at kommunen må dytte store mengder sensitive filer ut av huset. Dette understøtter også "sammenhengende tjenester" ved at andre autoriserte aktører kan abonnere på de samme hendelsene.

- **Overgangsløsning: Automatisert Innsending (Spor C)**:For å sikre fremdrift bør man støtte en modell der fagsystemene kan "pushe" data direkte til statlige mottakspunkter. Dette krever mindre endring i statlige IT-arkitekturer på kort sikt, men bør ses på som et steg på veien mot full API-basert deling.

## 9. Behov for videre arbeid

- **Dialog med SSB:** Avklare deres veikart for mottak av data og villighet til å gå fra "filmottak" til API-oppslag.
- **Informasjonsmodellering:** Videreføre arbeidet med felles begrepsutvalg slik at en "hendelse" betyr det samme i alle systemer.
- **Pilotering:** Teste ut Spor A+B på et avgrenset felt innen barnevern eller helsetjenester for å dokumentere faktisk reduksjon i tidsbruk.
