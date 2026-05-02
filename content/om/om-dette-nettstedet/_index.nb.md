---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: "23a6ec0b-a515-4db0-907c-7d96836d3dfd"
title: Om dette nettstedet
linkTitle: Om dette nettstedet
weight: 20

---
SAMT-BU Docs er et statisk dokumentasjonsnettsted utviklet som del av prosjektet SAMT-BU (Sammenhengende tjenester for barn og unge). Nettstedet er én av flere dokumentasjonskanaler i prosjektet og samler faglig innhold tilgjengelig for alle samarbeidspartnere. Nettstedet samler faglig dokumentasjon, arkitekturbeskrivelser, brukstilfeller og veiledninger på ett sted – tilgjengelig for alle samarbeidspartnere.

## Hva du finner her

Innholdet er under utvikling. Her er noe av det som er på gang.

- **Behov og brukstilfeller** – et antall nummererte use cases som beskriver de viktigste behovene digitaliseringen skal løse
- **Arkitektur og målbilde** – kapabilitetskart, tjenester, brukerreiser og prosesser
- **Løsninger** – teknisk dokumentasjon og veiledninger for de som bygger og forvalter plattformen
- **Rammeverk** – metodikk, juss, styring, standarder og begrepsapparat

## Teknisk plattform

Nettstedet er bygget med [Hugo](https://gohugo.io/) (statisk nettstedsgenerator) og publiseres via Cloudflare Pages. Innholdet skrives i Markdown og versjonshåndteres i Git. Tospråklig støtte (norsk og engelsk) er innebygd.

Innhold fra team-repoer monteres automatisk inn via Hugo Modules, og CMS-redigering er mulig direkte i nettleseren via en egen løsning for dette – uten at brukerne trenger teknisk kunnskap om Git eller Markdown.

## Innlogging og tilgang

For å redigere innhold logger du inn med en GitHub-konto. SAMT-BU Docs bruker en **GitHub App** – ikke en bred OAuth-tillatelse. Det betyr at appen kun får tilgang til de spesifikke repoene i SAMT-X-organisasjonen der appen er installert, ikke til andre repositorier på kontoen din.

Hvis du sender inn et endringsforslag (som bruker uten skrivetilgang), utfører en dedikert bot-konto (`samt-x-bot`) de tekniske GitHub-operasjonene på dine vegne. Ditt forslag registreres som en pull request med ditt GitHub-brukernavn, men boten håndterer selve skrivingen til repoet.

Du kan trekke tilbake tilgangen når som helst via GitHub-innstillingene dine (Settings → Applications → Authorized GitHub Apps).

En fullstendig risikovurdering med detaljer om arkitektur og kompenserende tiltak finnes i [Teknisk dokumentasjon → Risikovurdering](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/risikovurdering/).

## Se også

- [Hvordan bidra](/samt-bu-docs/om/hvordan-bidra/) – kom i gang med redigering og bidrag
- [SAMT-BU Docs – løsningsdokumentasjon](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/) – teknisk dokumentasjon og brukerveiledning for redaktører
