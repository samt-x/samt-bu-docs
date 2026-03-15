---
id: "6d076c0e-d83d-4590-945b-e8695201138e"
title: "3. Håndtering av D-nummer og ID-bytte"
linkTitle: "3. Håndtering av Dnr"
weight: 30
toc: true
# Gyldige statusverdier:
# ◍ Ny
# ◔ Tidlig utkast
# ◐ Pågår
# ◕ Til QA
# ⏺ Godkjent
# ⨂ Avbrutt
status: "Tidlig utkast"
last_editor: erikhag1git (Erik Hagen)

---

## Kort beskrivelse

- ID-håndtering av flyktninger og asylsøkere
- Bytte av ID
- Ivareta personens data og rettigheter når man bytter ID-nummer

### Hvem har spilt inn dette caset?

Bergen kommune.

## Problemet i dag

Innen oppvekst er det ingen fellesløsning for tildeling av ID-nummer for personer som ikke ennå har fått D-nummer eller F-nummer i folkeregisteret. Som regel får foreldre D-nummer i forbindelse med at de skal betale skatt, mens det kan ta lengre tid før barn får D-nummer eller fødselsnummer. I påvente av dette må kommunene registrere en rekke fiktive fødselsnummer etter egen forordning. Personobjektene oppstår altså potensielt med en rekke ulike identifikatorer rundt omkring i det offentlige.

### Hvor oppstår brudd i informasjonsflyt eller ansvar?

Kommunene gir tjenester til personer som ikke er registrert i folkeregisteret med D-nummer, eller F-nummer. Dermed blir kommuner tvunget, i hver sine sektorer, å opprette en eller mange fiktive versjoner av disse personobjektene i påvente av at disse personene får et ID-nummer i folkeregisteret. Det er ingen samkjøring av slike fiktive numre mellom sektorer eller mellom de ulike kommuner og fylkeskommuner.

## Aktører

### Berørte aktører

- Foreldre som mister tilganger, eller mister data
- Barn og elever som mister data

## Konsekvenser av dagens situasjon

Kommunene har plikt å gi personer en del tjenester, som barnehageplass og skoleplass, selv om de ikke har ID i folkeregisteret.

Når personer etter hvert får ID-nummer i folkeregisteret, er det ingen automatikk i at kommunen med sikkerhet kan si at nye personobjekter som importeres fra folkeregisteret med 100% sikkerhet er de samme som kommunen har registrert inn i de ulike systemer med fiktivt nummer. Kun likhet i navn og adresse kan gi en grad av indikasjon på dette. Feil kan i ytterste konsekvens skje. Det er litt enklere når barnet etter hvert får et D-nummer eller Fødselsnummer, for da følger som regel også foreldrerelasjonene med i dataflyten fra folkeregisteret. Dessverre skjer dette ofte lenge etter at foreldrene får slikt nummer i folkeregisteret.

Mange systemer støtter overgangen fra D-nummer til F-nummer ved at integrasjonen gir informasjon om endringen. Det muliggjør en automatikk i endringen, og da sikrer man potensielt at data ikke går tapt eller er utilgjengelig.

ID-nummeret er som regel den primære nøkkelen for personobjekter. Så uten automatikk eller god kontroll vil det typisk oppstå duplikater av personobjekter i flere systemer. Dette kan gjøre at informasjon ikke blir funnet, slik som vedtak, eller at foreldre eller elev mister data de har lagret i ulike IT-systemer.

Fiktive nummer gir heller ikke tilgang til innlogging i offentlige IT-systemer med ID-porten.

Helse har kommet lenger i en fellesløsning her, slik vi forstår det, og har noe som heter Hjelpenummer. Les mer om det her, samt utfordringene de beskriver som godt kan sammenlignes med andre offentlige sektorer:
https://www.nrk.no/norge/darlig-id-system-en-pasientfare-1.11425318

## Ønskesituasjon

Det blir mulig å opprette Identiteter i Folkeregisteret, eller i FIKS folkeregister som blir felles for alle sektorer. Det legges inn noe automatikk som hindrer at kommuner oppretter duplikater, slik som kontroll av navn, fødselsdato og bostedsadresse. Det er mulig å registre inn de samme data som på personer som har fødselsnummer, slik som foreldre/barn-relasjoner. Foreldreansvar settes som ukjent.

Denne ID'en etableres som ett fullverdig medlem av ID-håndtering og gir tilgang til bruk av ID-porten. Ved overgang til D-nummer eller F-nummer sikrer systemet at det fiktive nummer (kall det H-nummer som i Helse) blir erstattet og varslet ut i integrasjoner slik at andre systemer kan gjennomføre en kontrollert og automatisert overgang til nytt nummer. Siden Helse allerede har et slikt system, hadde det vært en fordel om dette nye systemet kan hente H-nummer med data fra helse for å unngå duplikate H-nummer på tvers av Helse og andre sektorer.

## Innsiktsarbeid

Enklere brukerreiser for ansatte, foresatte, elever og studenter gjennom læringsløpet - fra barnehage til grunnskole, videregående og høyere utdanning.

## Berørte prosjektmål

- Felles informasjonsmodeller og standardiserte grensesnitt som på sikt dekker «alle» områder og sektorer.
- Skalering og overføring av prosjektets læring og produkter til andre områder og sektorer, etter pilotering i dette prosjektet.
