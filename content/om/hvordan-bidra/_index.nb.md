---
id: "1e0d2050-f885-496d-8ab4-8bdc287697e8"
title: "Hvordan bidra"
linkTitle: "Hvordan bidra"
weight: 30
last_editor: erikhag1git (Erik Hagen)

---

Dette nettstedet er åpent for bidrag fra alle samarbeidspartnere i SAMT-BU-prosjektet. Det finnes flere måter å bidra på – se oversikten under. For de fleste fagpersoner og redaktører er **innebygd redigering i nettleseren** den anbefalte veien inn.

| Metode | Passer for | Krever |
|--------|-----------|--------|
| [Innebygd editor](#anbefalt-innebygd-redigering-i-nettleseren) | Fagpersoner og redaktører | GitHub-konto + skrivetilgang |
| [GitHub-redigering](#alternativ-redigering-direkte-p-github) | Enkeltendringer, tekniske brukere | GitHub-konto + Markdown |
| [Lokal oppsett](#alternativ-lokal-oppsett-for-utviklere) | Strukturelle endringer, utviklere | Hugo + Git installert |

---

## Anbefalt: Innebygd redigering i nettleseren

Du redigerer innhold direkte i nettleseren i et visuelt tekstverktøy – ingen Markdown- eller Git-kunnskap nødvendig.

### Hva du trenger

- En **GitHub-konto** (opprett gratis på [github.com](https://github.com))
- **Skrivetilgang** til riktig repo – kontakt en administrator for å få dette første gang

### Redigere en eksisterende side

1. Gå til siden du vil redigere
2. Klikk **«Endre»**-menyen øverst til høyre i headeren
3. Velg **«Rediger dette kapitlet»**
4. Logg inn med GitHub-kontoen din hvis du ikke allerede er innlogget (popup-vindu)
5. Gjør endringene dine i tekstfeltet
6. Klikk **«Lagre»**

**Tips:** Bilder kan limes direkte inn i tekstfeltet (Ctrl+V eller høyreklikk → Lim inn) – det finnes foreløpig ingen egen bildeknapp i verktøylinjen.

Nettstedet oppdateres automatisk etter lagring. En statusindikator nede til venstre i skjermen holder deg oppdatert underveis.

### Statusindikator og jobbhistorikk

**Indikatoren nede til venstre** er alltid synlig og viser gjeldende tilstand:

| Tilstand | Tekst | Betyr |
|----------|-------|-------|
| Ingen pågående jobb | «Byggehistorikk» | Klikk for å se tidligere byggejobber |
| Lagret, venter på bygg | «N endringer bygges…» | Endringen er sendt – bygg er i gang eller i kø |
| Ferdig | «Endringer publisert – klikk for å laste inn» | Klikk for å se den oppdaterte siden |

Klikker du på indikatoren åpnes en **jobbhistorikk-dialog** som viser de siste byggejobber med status, tidspunkt og lenke til GitHub Actions. Her kan du se:
- 🔄 Kjørende jobb – med antall sekunder siden den startet
- 🕐 Jobb i kø – venter på tur
- ✅ Fullført
- ✅ (grå) Avløst av nyere bygg – se forklaring under

#### Om byggetid og køer

Nettstedet bygges av GitHub Actions. Normalt tar et bygg **ca. 1 minutt**. Hvis du eller andre lagrer flere sider raskt etter hverandre, kan ventetiden bli lengre fordi byggejobber kjøres én om gangen:

- **2 lagringer etter hverandre:** andre jobb venter til første er ferdig – totaltid ca. 2 min
- **3 eller flere raske lagringer:** GitHub kan *avløse* eldre jobber i kø med den nyeste. Det betyr at en jobb i historikken kan vises som «Avløst» i stedet for fullført – dette er normalt og betyr ikke at noe gikk galt. Alle lagrede endringer er registrert i Git og vil bli publisert av den siste jobben som kjøres.

> **Kort sagt:** Ser du grå hake og teksten «Avløst» i jobbhistorikken, er ikke endringen tapt – den ble publisert av en nyere jobb.

### Opprette en ny side

1. Gå til siden du vil plassere den nye siden ved siden av (søsken) eller under (underkapittel)
2. Klikk **«Endre»** og velg:
   - **«Nytt kapittel etter dette»** – ny side på samme nivå
   - **«Nytt underkapittel»** – ny side ett nivå ned
3. Fyll inn tittel og eventuelt innhold i dialogen
4. Klikk **«Lagre»**

---

## Alternativ: Redigering direkte på GitHub

Passer for enkeltendringer og mindre rettelser uten lokal installasjon. Krever GitHub-konto og kjennskap til Markdown.

**Slik gjør du det:**

1. Gå til siden du vil redigere på [samt-x.github.io/samt-bu-docs](https://samt-x.github.io/samt-bu-docs/)
2. Klikk lenken **«Rediger på GitHub»** nederst på siden
3. Gjør endringene dine i Markdown-feltet
4. Rull ned til **«Commit changes»**
5. Skriv en kort beskrivelse av hva du endret
6. Velg **«Create a new branch and start a pull request»** (anbefalt) eller commit direkte til `main` hvis du har rettigheter
7. Klikk **«Propose changes»** – en redaktør vil se over og godkjenne

Siden publiseres automatisk innen et minutt etter at endringen er godkjent.

---

## Alternativ: Lokal oppsett (for utviklere)

Dette alternativet gir deg et fullt lokalt arbeidsmiljø der du kan forhåndsvise alle endringer i nettleseren mens du skriver. Anbefalt for strukturelle endringer, nytt innhold i større omfang eller teknisk utvikling.

### Hva du trenger

| Verktøy | Versjon | Formål |
|---------|---------|--------|
| [Git](https://git-scm.com/) | Siste stabile | Versjonskontroll |
| [Hugo Extended](https://gohugo.io/) | 0.155.3 eller nyere | Nettstedsgenerator |
| [Go](https://go.dev/) | 1.21 eller nyere | Kreves av Hugo Modules |
| Teksteditor | – | [VS Code](https://code.visualstudio.com/) anbefales |

### Installasjon på Windows

```powershell
winget install --id Git.Git
winget install --id Hugo.Hugo.Extended
winget install --id GoLang.Go
winget install --id Microsoft.VisualStudioCode
```

Start terminalen på nytt etterpå, slik at de nye programmene er tilgjengelige i PATH.

**Verifiser installasjonen:**

```powershell
git --version
hugo version
go version
```

### Installasjon på macOS

```bash
brew install git hugo go
```

### Installasjon på Linux (Ubuntu/Debian)

```bash
sudo apt install git golang
# Hugo Extended hentes fra GitHub Releases (apt-versjonen er ofte for gammel):
wget https://github.com/gohugoio/hugo/releases/download/v0.155.3/hugo_extended_0.155.3_linux-amd64.deb
sudo dpkg -i hugo_extended_0.155.3_linux-amd64.deb
```

### Klone repoet

```bash
git clone --recurse-submodules https://github.com/SAMT-X/samt-bu-docs.git
cd samt-bu-docs
hugo mod download
```

`--recurse-submodules` sørger for at temaet (`hugo-theme-samt-bu`) lastes ned. `hugo mod download` henter innholdsmoduler fra de andre repoene.

### Start lokal forhåndsvisning

```bash
hugo server
```

Åpne [http://localhost:1313/samt-bu-docs/](http://localhost:1313/samt-bu-docs/) i nettleseren. Siden oppdaterer seg automatisk når du lagrer en fil.

### Filstruktur – der innholdet bor

```
content/
  om/                    ← «Om»-seksjonen
  behov/                 ← Behov (use cases)
  pilotering/            ← Piloter
  arkitektur/            ← Arkitektur
  loesning/              ← Løsninger
  rammeverk/             ← Rammeverk
  informasjonsmodeller/  ← Informasjonsmodeller
  innsikt/               ← Felles innsikt
  teams/                 ← Teams (innholdsmodul)
  utkast/                ← Utkast og innspill (innholdsmodul)
```

Hvert kapittel er en **mappe** med to filer:

```
content/om/om-samt-bu/
  _index.nb.md    ← Norsk innhold
  _index.en.md    ← Engelsk innhold
```

### Skrive innhold

Innholdsfiler er vanlige Markdown-filer med et lite felt øverst (frontmatter):

```markdown
---
title: "Sidetittel"
weight: 30
---

Her begynner innholdet ditt i vanlig Markdown.

## Overskrift

En avsnitt med **fet tekst** og *kursiv tekst*.
```

- `title` – sidetittel som vises i menyen og øverst på siden
- `weight` – sorteringsrekkefølge (lavere tall = høyere opp i menyen)
- `draft: true` – legg til dette for å skjule siden fra publisering inntil den er klar

### Lagre og publisere endringer

```bash
git add content/sti/til/filen/_index.nb.md
git commit -m "Kort beskrivelse av hva du endret"
git push
```

GitHub Actions bygger og publiserer automatisk etter 1–2 minutter.

> **Uten skrivetilgang til repoet?** Opprett en *pull request* i stedet:
> `git checkout -b mitt-bidrag` → gjør endringer → `git push origin mitt-bidrag` → åpne PR på GitHub.

### Nyttige kommandoer

| Kommando | Beskrivelse |
|----------|-------------|
| `hugo server` | Start lokal server med live-reload |
| `hugo server -D` | Inkluder også utkast (`draft: true`) |
| `hugo` | Bygg til `public/` (sjekk for feil) |
| `git pull` | Hent siste endringer fra GitHub |
| `hugo mod get -u` | Oppdater alle innholdsmoduler til siste versjon |
