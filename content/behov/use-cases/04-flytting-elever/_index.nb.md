---
id: "105fab2b-19bb-47e2-a292-44cd50cbf7d6"
title: 4. Flytting av elever i skoleåret mellom kommuner/fylkeskommuner
linkTitle: 4. Flytting av elever
weight: 5
toc: true
# Gyldige statusverdier:
# ◍ Ny
# ◔ Tidlig utkast
# ◐ Pågår
# ◕ Til QA
# ⏺ Godkjent
# ⨂ Avbrutt
status: Tidlig utkast
last_editor: erikhag1git
---
## 1. Mål

Målet er å sikre at nødvendig informasjon om en elev følger eleven digitalt og automatisk ved flytting mellom kommuner. Dette skal sikre kontinuitet i opplæringen, spesielt for sårbare barn, og redusere tiden fra innflytting til barnet får et tilrettelagt tilbud i den nye skolen.

## 2. Aktører

- **Elev/Foreldre:** Flytter og melder innflytting i ny kommune.
- **Skoleadministrativt ansvarlig (Fraflyttingskommune):** Ansvarlig for å avslutte elevforholdet og tilgjengeliggjøre dokumentasjon.
- **Skoleleder/Lærer (Tilflyttingskommune):** Mottaker av eleven som trenger rask innsikt i elevens historikk og behov.
- **Fagsystemer (f.eks. Vigilo, Visma Flyt Skole, IST):** Systemene som skal utveksle dataene.
- **Folkeregisteret (FREG):** Kilden som trigger flyttehendelsen.

## 3. Forutsetninger

- Eleven er registrert med flytting i Folkeregisteret eller foreldrene har takket ja til skoleplass i ny kommune.
- Det foreligger lovhjemmel for deling av taushetsbelagt informasjon (eller samtykke fra foreldre der det kreves).
- Felles standarder for utveksling av elevmapper (f.eks. etter SIKT- eller KS-standarder).

## 4. Trigger

En flyttehendelse registreres, enten ved at foreldre søker skoleplass i ny kommune, eller via en automatisk melding fra Folkeregisteret om adresseendring.

## 5. Hovedforløp (Den moderne datastrømmen)

1. **Flyttevarsel:** Tilflyttingskommunens fagsystem mottar melding om at en ny elev flytter til kommunen.
2. **Hendelsesnotifikasjon (Spor A):** Tilflyttingskommunen sender en forespørsel (via en felles kjerne) til fraflyttingskommunen om tilgang til elevens digitale mappe.
3. **Automatisk kontroll og autorisasjon:** Fraflyttingskommunens system verifiserer identitet og hjemmel for deling.
4. **Datahenting via API (Spor B):** Tilflyttingskommunen henter nødvendig "grunnpakke" (karakterer, fravær, gruppetilhørighet) og eventuell "utvidet pakke" (IOP, sakkyndige vurderinger) direkte fra kildesystemet i fraflyttingskommunen.
5. **Klargjøring:** Lærer ved den nye skolen får et varsel i sitt fagsystem: "Ny elev starter mandag – dokumentasjon er klar til gjennomgang."

## 6. Alternative forløp

- **6a. Behov for samtykke:** Dersom dataene er av en slik art at samtykke kreves, trigges en melding til foreldre i en innbyggerportal for digital signering før dataene frigis.
- **6b. Manglende digital modenhet:** Dersom fraflyttingskommune ikke har API-støtte, genereres en standardisert eksportfil (Spor C) som sendes via sikker digital post til den nye skolen.

## 7. Gevinster

- **Barnets beste:** Eleven opplever en tryggere overgang uten "tomrom" i oppfølgingen.
- **Ressursbesparelse:** Lærere slipper å bruke uker på å etterlyse dokumentasjon og kartlegge eleven på nytt.
- **Datakvalitet:** Informasjonen er korrekt og oppdatert, ikke basert på muntlige overleveringer eller utdaterte papirkopier.

## 8. Innspill til løsningsvalg

For at dette skal fungere nasjonalt, må vi unngå at hver kommune lager egne integrasjoner mot alle andre.

- **Anbefalt løsning: Hybrid Hendelsesdrevet API-modell (Spor A+B)**:Vi bør bruke en arkitektur der flyttingen fungerer som en *hendelse* som trigger en rettighetsstyrt *henting* av data. Ved å bruke "Notification-first", kan vi sikre at sensitive data kun flyttes når det er et bekreftet behov hos mottakeren.
- **Standardisert Elevmappe:** Det er kritisk at innholdet i det digitale flyttelasset er standardisert (semantisk samhandling). Det hjelper lite å flytte dataene hvis kjernebegreper er definert ulikt i de to systemene.

## 9. Behov for videre arbeid

- **Juridisk avklaring:** Sikre at personvernforordningen (GDPR) er ivaretatt ved automatisk overføring av sensitive elevdata mellom kommuner.
- **Leverandørdialog:** Koordinere med de store skoleleverandørene for å sikre at de implementerer de samme API-standardene.
- **Kobling mot barnevern/PPT:** Utrede om flyttehendelsen også bør trigge tilsvarende sømløs overføring i andre sektorer for barn med sammensatte behov.
