---
id: e0d42db3-b997-4bcc-9bf5-4da622c18429
title: 22. Analysedata fra barnehage til voksenopplæring
linkTitle: "22. Analysedata for \"hele løpet\""
weight: 220
toc: true
status: Tidlig utkast
# Gyldige statusverdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
last_editor: erikhag1git (Erik Hagen)
---
## Kort beskrivelse

Det er ønskelig med data fra hele utdanningssektoren som kan si noe om «hvordan det gikk» for ulike elever – fra barnehage til voksenopplæring. Data benyttes på aggregert nivå, men må basere seg på individuelle data.

Vestland FK har etablert en løsning der det gjøres analyser av data fra blant annet VIGO, som de deler med kommunene i fylket. Dette caset tar utgangspunkt i det Vestland FK allerede har fått til, og peker på behovet for å utvide dette til å dekke hele utdanningsløpet – og gjøre tilsvarende løsninger tilgjengelig for flere.

### Hvem har spilt inn dette caset?

Vestland FK.

## Problemet i dag

Sosial bakgrunn, resultater og innsats henger sammen gjennom hele utdanningsløpet – fra barnehage til høyere utdanning og arbeidsliv. For å kunne se den store sammenhengen og intervenere der «problemene dukker opp», er det behov for data som dekker hele løpet på individnivå (aggregert for analyse). I dag finnes ikke dette.

### Hvor oppstår brudd i informasjonsflyt eller ansvar?

Brudd oppstår særlig:

- mellom barnehage og grunnskole – ulike systemer, ulike eiere, ingen felles dataflyt
- mellom grunnskole og videregående – kommunalt og fylkeskommunalt ansvar deler seg her
- mellom videregående og høyere utdanning – fylkeskommunalt og statlig ansvar
- mellom utdanning og arbeidsliv – svært begrenset kobling

## Aktører

### Sluttbrukere (av analysedata)

- Kommuner – for å vurdere effekt av tiltak og planlegge ressursbruk
- Fylkeskommuner – for å følge elevflyt og utdanningsresultater over tid
- Politisk ledelse på ulike nivåer – for beslutningsgrunnlag
- Barn, unge og foresatte – indirekte, gjennom bedre tilpassede tjenester

### Ansatte i tjenestene

- Analytikere og planleggere i kommuner og fylkeskommuner
- Skoleledelse og rådgivere

### Fagsystemleverandører

- Leverandører av barnehage- og skoleadministrative systemer (VIGO, IST, Visma m.fl.)
- Leverandører av analyseplattformer og datadelingstjenester

### Premissgivere

#### Direktorater

- **Utdanningsdirektoratet** – fagdirektorat for grunnopplæringen; forvalter sentrale utdanningsdata
- **Statistisk sentralbyrå (SSB)** – forvalter befolknings- og utdanningsstatistikk på individnivå
- **Digitaliseringsdirektoratet** – tverrsektoriell premissgiver for datadeling og samhandling

#### Departementer

- **Kunnskapsdepartementet** – overordnet ansvar for utdanningssektoren
- **Digitaliserings- og forvaltningsdepartementet** – overordnet ansvar for datadeling og tverrsektorielle initiativ

### Tjenesteleverandører

- **Kommuner** – eier og forvalter data fra barnehage og grunnskole
- **Fylkeskommuner** – eier og forvalter data fra videregående opplæring

### Samordnende og støttende aktører

- **KS og KS Digital** – koordinerer kommunesektoren og leverer felles digitale løsninger
- **Sikt** – leverer og forvalter fellestjenester i utdanningssektoren

## Konsekvenser av dagens situasjon

### For sluttbrukere (kommuner, fylkeskommuner og politisk ledelse)

- Liten oversikt over sammenhengen mellom ulike faser i livet
- Vanskelig å avdekke mønstre og vurdere effekten av tiltak på tvers av utdanningsnivåer
- Beslutninger må tas på svakere datagrunnlag enn nødvendig

### For ansatte i tjenestene

- Analyser må bygges manuelt på tvers av systemer uten felles infrastruktur
- Mye tid går med til datainnhenting og sammenstilling fremfor analyse

### For organisasjonene

- Ineffektiv ressursbruk – samme arbeid gjøres parallelt i mange kommuner og fylkeskommuner
- Vanskeligere å samarbeide om felles innsikt på tvers av kommuner og forvaltningsnivåer

### På systemnivå

Uten data som dekker hele utdanningsløpet er det vanskelig å måle effekten av langsiktige tiltak, identifisere risikogrupper tidlig nok, eller planlegge målrettet for en hel befolkningskohortt fra barnehage til arbeidsliv.

## Ønskesituasjon

I en ønsket situasjon kan kommuner og fylkeskommuner enkelt se sammenhengende data fra barnehage, grunnskole, videregående og videre – på et aggregert nivå som ivaretar personvern, men som likevel er basert på individdata. Dette gir et reelt grunnlag for å vurdere effekten av tiltak over tid, avdekke mønstre på tvers av utdanningsnivåer og planlegge ressursbruk målrettet.

Analysekapasitet som i dag bare finnes hos ressurssterke fylkeskommuner (som Vestland FK), bør gjøres tilgjengelig for alle kommuner – uavhengig av størrelse og egne tekniske ressurser.

## Innspill til løsningsvalg

### Vestland FKs eksisterende løsning som utgangspunkt

Vestland FK har etablert en løsning der data fra blant annet VIGO analyseres og deles med kommunene i fylket. Et eksempel er elevflyten i videregående utdanning, der man år for år kan se status for elevene: hvem som starter med hva, hvor mange som har progresjon, omvalg, sluttere og sluttkompetansen. Dette kan filtreres på avgiverkommune, avgiver ungdomsskole, grunnskolepoeng, fraværsmengde, kjønn m.m.

I en utvidet løsning kan tilsvarende data fra barnehage og grunnskole plasseres til venstre i dette bildet, og eventuell høyere utdanning/jobbstatus til høyre – slik at hele livsløpet er synlig i én sammenhengende analyse.

![Eksempel på elevflyt i videregående utdanning i Vestland FK](elevflyt-vestland.png)### Felles kommunal dataplattform – KS Digital / Azure Databricks

KS Digital arbeider med en felles kommunal dataplattform basert på Azure Databricks. En slik plattform vil kunne gi kommuner og fylkeskommuner tilgang til en felles infrastruktur for lagring, prosessering og analyse av data på tvers av tjenester og sektorer – uten at den enkelte kommune må bygge og drifte dette selv.

> **⚠ Merknad:** Detaljene om KS Digitals konkrete planer, fremdrift og omfang for denne plattformen er ikke verifisert i dette dokumentet. Avsnittet bør oppdateres med referanse til offisielle kilder og avklaring av hva som er planlagt vs. besluttet.

Dersom en slik plattform realiseres, vil den være et naturlig fundament for caset om analysedata for hele løpet – ved at data fra barnehage, grunnskole, videregående og videre kan sammenstilles i én felles infrastruktur med felles tilgangsstyring og personvernmekanismer.

## Innsiktsarbeid

Caset bygger på innspill fra Vestland FK, som har praktisk erfaring med analyse av VIGO-data delt med kommuner. Erfaringene er relevante som modell for hva som er mulig, og hva som kreves av datainfrastruktur og avtaleverk.

## Berørte prosjektmål

- Felles informasjonsmodeller og standardiserte grensesnitt som på sikt dekker «alle» områder og sektorer
- Gjenbrukbare løsninger og fellesløsninger – analysekapasitet tilgjengelig for alle kommuner
- Enklere brukerreiser for ansatte, foresatte, elever og studenter gjennom læringsløpet
- Samarbeid og innovasjon på tvers av offentlige aktører i økosystemet
- Langsiktige mål om livslang læring
- Skalering og overføring av prosjektets læring og produkter til andre områder og sektorer
