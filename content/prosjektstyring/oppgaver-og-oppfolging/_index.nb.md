---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 5c5afb34-e520-461e-813b-5de086478937
title: "Oppgaver og oppfølging"
linkTitle: "Oppgaver og oppfølging"
weight: 25
---

Her finner du lenkene du trenger for å følge opp arbeidet i SAMT-BU: dine egne oppgaver, brettene til delprosjektene, og etter hvert porteføljen for hele prosjektet. Oppgavene og brettene ligger i GitHub og er åpne for alle. Bare søkene etter dine egne oppgaver krever at du er logget inn, fordi GitHub må vite hvem du er.

Hvordan oppgavestyringen er bygd opp, og reglene vi følger, står under [Oppgavestyring](https://docs.samt-bu.no/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/).

## Mine oppgaver

Ferdige søk på tvers av alle repoer og brett i SAMT-BU. Legg dem gjerne inn som bokmerker. Begge krever at du er logget inn på GitHub.

| Søk | Viser |
|---|---|
| [Mine åpne oppgaver](https://github.com/issues?q=is%3Aissue%20is%3Aopen%20assignee%3A%40me%20org%3Asamt-x) | Åpne oppgaver som er tildelt deg (Assignee) |
| [Oppgaver der jeg er nevnt](https://github.com/issues?q=is%3Aissue%20is%3Aopen%20mentions%3A%40me%20org%3Asamt-x) | Åpne oppgaver der noen har nevnt deg med @ |

Søkene viser bare oppgaver der du står som **Assignee** eller er nevnt. Derfor er det viktig at oppgaver tildeles.

Er du **ansvarlig** for oppgaver i arkitekturgruppa, ser du dem i visningen [By responsible](https://github.com/orgs/samt-x/projects/5/views/3) i Project 5. Et søk etter ansvar på tvers av alle brett er ikke mulig ennå, fordi GitHubs søk ikke ser feltene på brettene. Det kommer med samlebrettet, se [veikartet](https://docs.samt-bu.no/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/veikart/oversikt-for-den-enkelte/).

## Oppgaver som trenger oppfølging

| Søk | Viser |
|---|---|
| [Åpne oppgaver som ingen er tildelt](https://github.com/search?q=is%3Aissue%20is%3Aopen%20no%3Aassignee%20org%3Asamt-x&type=issues) | Oppgaver uten Assignee, som kan falle mellom to stoler. Virker uten innlogging. |
| [Blokkerte oppgaver](https://github.com/search?q=is%3Aissue%20is%3Aopen%20label%3Ablocked%20org%3Asamt-x&type=issues) | Åpne oppgaver med merkelappen blocked, som venter på noe utenfor oppgaven. Hva de venter på, står i en kommentar. Virker uten innlogging. |

## Prosjektbrettene

Et **prosjektbrett** er et prosjekt i GitHub (GitHub Projects): en samling oppgaver med felles felt, som status, ansvarlig og frist. Samme brett kan vises på flere måter, og hver visning ligger i en egen fane på brettet:

- **Kanban-brett** (i GitHub: Board): én kolonne per steg i arbeidsflyten, for eksempel Ny, Pågår og Ferdig. Hver oppgave er et kort som flyttes fra venstre mot høyre etter hvert som arbeidet går framover. Kolonnene kan også deles inn etter et annet felt, for eksempel ansvarlig eller prioritet.
- **Tabell** (Table): én rad per oppgave, med feltene som kolonner. Egner seg til å sortere og filtrere.
- **Tidslinje** (Roadmap): oppgavene plassert langs en tidsakse etter dato.

Flytter du et kort til en annen kolonne, endres feltet kolonnene bygger på, som oftest status. Endringen vises i alle visningene, fordi det er den samme oppgaven.

Hvert delprosjekt har sitt eget prosjektbrett, med egne statuser og felt.

| Delprosjekt | Brett |
|---|---|
| Pilot 1 – Overgang ungdomsskole videregående | [Project 1](https://github.com/orgs/samt-x/projects/1) |
| Pilot 2 – Valg av utdanningsløp | [Project 2](https://github.com/orgs/samt-x/projects/2) |
| Pilot 3 – Flytting av barn og unge i skoleåret | [Project 4](https://github.com/orgs/samt-x/projects/4) |
| Pilot 4 – Vitnemål | [Project 3](https://github.com/orgs/samt-x/projects/3) |
| Pilot 5 – Id-er i utdanning | [Project 9](https://github.com/orgs/samt-x/projects/9) |
| Pilot 6 – Foreldres tilgang til data | [Project 10](https://github.com/orgs/samt-x/projects/10) |
| Rammeverk og generisk arkitektur (arkitekturgruppa) | [Project 5](https://github.com/orgs/samt-x/projects/5), med visningene [By responsible](https://github.com/orgs/samt-x/projects/5/views/3) og [My tasks](https://github.com/orgs/samt-x/projects/5/views/7) (krever innlogging) |
| Informasjonsmodeller | [Project 6](https://github.com/orgs/samt-x/projects/6) |

Brettene har i dag ulike statuser og visninger. Det arbeides med felles maler, slik at alle brettene kan rapporteres samlet. Se [veikartet for oppgavestyringen](https://docs.samt-bu.no/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/veikart/felles-oppsett/).

## SAMT-BU-porteføljen

Porteføljen gir oversikt over hele prosjektet, med ett kort per pilot, produkt og arbeidsområde: hvem som eier det, hvilken fase det er i, og hvordan det går. Porteføljebrettet er ikke laget ennå. Se [veikartet](https://docs.samt-bu.no/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/veikart/portefoljestyring/).

Når brettet er på plass, beskrives selve styringen her: hva som er i porteføljen, hvem som eier hva, og hvor ofte porteføljen gjennomgås.
