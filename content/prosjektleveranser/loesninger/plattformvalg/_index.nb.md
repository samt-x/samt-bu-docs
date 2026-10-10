---
title: "Plattformvalg: GitHub"
linkTitle: "Plattformvalg: GitHub"
weight: 5

---

SAMT-BU bruker GitHub til innhold, oppgaver og samarbeid. Denne siden forklarer hvorfor, hva valget koster med tanke på digital suverenitet, og hva som skal til for å velge annerledes. Andre sider i dokumentasjonen henviser hit i stedet for å gjenta begrunnelsen.

**Status: foreløpig valg.** GitHub har vært brukt siden dokumentasjonsarbeidet startet i februar 2026. Valget er ført i [beslutningsloggen](/prosjektstyring/beslutningslogg/2026-10-11-plattformvalg-github/) og kan tas opp igjen.

## Hva GitHub brukes til

| Bruk | Eksempel |
|---|---|
| Innhold | Alle sidene på docs.samt-bu.no ligger som tekstfiler i repoer i organisasjonen samt-x |
| Oppgaver | Issues og prosjektbrett, se [Oppgavestyring](/prosjektleveranser/loesninger/styringsloesninger/oppgavestyring/) |
| Redigering på nettstedet | Innlogging, lagring og forslag til endring går mot GitHub, se [SAMT-BU Docs](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/) |
| Bygging og publisering | GitHub Actions bygger nettstedet ved hver endring, og Cloudflare Pages publiserer det |
| Tilgang | Team i organisasjonen styrer hvem som kan endre hva |

## Hvorfor GitHub

- **Der samarbeidspartnerne er.** GitHub er mest brukt i Digdir og blant samarbeidspartnerne. Altinn, Felles datakatalog og de fleste synlige prosjekter med åpen kildekode i norsk offentlig sektor ligger der.
- **Ingen terskel for å komme i gang.** Mange deltakere har allerede konto, og bruken er gratis for åpne repoer.
- **Modent økosystem.** Verktøy, integrasjoner og dokumentasjon finnes for nesten alt prosjektet trenger.

Valget er pragmatisk, ikke nødvendigvis det arkitektonisk sterkeste.

## Hva valget koster: digital suverenitet

GitHub eies av Microsoft og er underlagt amerikansk lov, blant annet CLOUD Act. GitHub er ikke åpen kildekode, og kan ikke driftes i egen regi i en norsk eller europeisk infrastruktur uten lisens fra Microsoft.

For et prosjekt i offentlig sektor betyr det at

- prosjektets arbeidsflate er avhengig av én kommersiell leverandør utenfor EU/EØS
- vilkår, priser og funksjoner kan endres uten at prosjektet har innflytelse
- innholdet er offentlig i dag, men ikke-offentlig eller sensitivt innhold bør ikke legges der uten en egen vurdering

Det samme gjelder **Cloudflare**, som publiserer nettstedet og håndterer innloggingen. Cloudflare er også et amerikansk selskap. Et bytte av git-plattform løser derfor ikke suverenitetsspørsmålet for nettstedet alene. Publiseringen må vurderes for seg.

Så lenge innholdet er åpent og kan flyttes, vurderer vi risikoen som akseptabel. Det er grunnen til at valget er foreløpig.

## Docs-løsningen og plattformvalget

Nettstedet docs.samt-bu.no er den delen av prosjektet som er tettest knyttet til plattformvalget. Den er satt sammen av lag med svært ulik binding:

| Lag | Bundet til | Kan flyttes? |
|---|---|---|
| Innhold (Markdown-filer) og bygging (Hugo) | Ingenting | **Ja**, uten endringer |
| Innholdsmoduler | Adresser på formen github.com/SAMT-X/… | **Ja**, adressene byttes |
| Redigering, forslag til endring og behandling av forslag | GitHubs programmeringsgrensesnitt, rundt 36 kall i temaet | **Må skrives om** |
| Innlogging | GitHub App og en Cloudflare Worker | **Må skrives om.** Med GitLab trengs Workeren trolig ikke. |
| Publisering | Cloudflare Pages | **Eget valg**, kan byttes uavhengig av git-plattformen |

Den innebygde redigeringen er bygget for prosjektet og gjør at deltakere uten Git-kunnskap kan bidra. Den er også den største bindingen. Se [SAMT-BU Docs](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/) for hvordan løsningen er bygget.

## Alternativer

Arbeidsformen – innhold som tekst i git, oppgaver som saker, endringer som forslag – er ikke knyttet til GitHub. Den samme arbeidsformen finnes i andre git-baserte løsninger:

| Løsning | Kjennetegn |
|---|---|
| **GitLab** | Samme modell som GitHub. Community Edition er åpen kildekode og kan driftes i egen regi. Har hierarkisk tilgangsstyring (grupper og undergrupper) som passer prosjekter med mange delprosjekter. EU-kommisjonen driver [code.europa.eu](https://code.europa.eu/) på GitLab. Merk at tjenesten GitLab.com også drives av et amerikansk selskap. Fordelen for suverenitet kommer først ved egen drift eller drift hos en europeisk aktør. |
| **Forgejo** | Lettere løsning med åpen kildekode, laget for egen drift og styrt av et fellesskap. |
| **Codeberg** | Europeisk, ideell tjeneste bygget på Forgejo. |

For lignende prosjekter i offentlig sektor bør en løsning som kan driftes i egen regi vurderes som førstevalg.

## Hva som skal til for å bytte

| Del | Kan flyttes? |
|---|---|
| Innholdet (tekstfiler og historikk) | **Ja**, uten endringer. Git er det samme overalt. |
| Oppgaver (issues og kommentarer) | **Delvis.** GitLab har innebygd import fra GitHub, men lenker og nummer endres. |
| Prosjektbrett | **Nei.** Må bygges opp igjen. Enkelte funksjoner i GitLab krever betalt versjon. |
| Redigering og innlogging på nettstedet | **Nei.** Må skrives om, se [Docs-løsningen](#docs-løsningen-og-plattformvalget). |
| Byggeskript | **Delvis.** GitHub Actions må oversettes til GitLab CI. Skriptene er korte. |

Innholdet, som er det viktigste, er altså ikke låst. Det som er låst, er verktøyene rundt.

### Hvor stort er et bytte?

Et bytte har to deler, og de har endret seg ulikt.

**Den tekniske delen er blitt vesentlig mindre.** Med KI-assistert utvikling er det å skrive om redigeringen mot et nytt programmeringsgrensesnitt, oversette byggeskript og flytte innhold en avgrenset jobb. Begrepene er de samme: GitLab har commits, grener og merge requests der GitHub har pull requests. Grovt anslått dreier det seg om dager til et par uker med konsentrert arbeid, ikke måneder. **Anslaget er ikke testet.**

**Den organisatoriske delen er uendret, og den er nå den største:**

- **Hvem skal drifte?** Suverenitet krever egen drift eller en europeisk driftsaktør. Det er en beslutning og en kostnad som ligger utenfor prosjektet.
- **Alle deltakerne må få nye kontoer** og lære et nytt sted å jobbe. Mange av dem er ikke tekniske.
- **Erfaringer må gjøres på nytt.** Det gjelder for eksempel hvordan varsler fungerer, tilgangsmodell og risikovurdering.
- **Tidspunktet:** Et bytte midt i et prosjekt med flere aktive piloter er en risiko i seg selv.

Et bytte er altså fortsatt et større tiltak, men flaskehalsen er ikke lenger koden.

**Slik kan anslaget gjøres pålitelig:** Et avgrenset forsøk på to–tre dager, der ett innholdsrepo speiles til GitLab og innlogging og lagring porteres for det repoet. Da har vi et tall vi kan stå inne for, i stedet for et anslag.

## Når valget bør tas opp igjen

- Prosjektet skal håndtere ikke-offentlig eller sensitivt innhold
- Oppdragsgiver eller Digdir stiller krav til digital suverenitet eller drift i Norge eller EU
- Prosjektets resultater skal over i varig forvaltning
- En felles offentlig git-plattform blir tilgjengelig
- GitHub endrer vilkår eller priser vesentlig

## Mer om temaet

- [Samskaping → Oppgavestyring](/utkast/temaer/samskaping/oppgavestyring/) drøfter hvorfor git-baserte plattformer passer for samarbeid mellom likeverdige organisasjoner
- [Konsept for GitHub-organisasjoner og repoer](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/github-struktur/) beskriver hvordan organisasjonen samt-x er satt opp, og hvordan valget påvirket teknikken bak docs.samt-bu.no
