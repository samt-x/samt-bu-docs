---
id: "1e0d2050-f885-496d-8ab4-8bdc287697e8"
title: "Hvordan bidra"
linkTitle: "Hvordan bidra"
weight: 30
last_editor: Erik Hagen

---

Dette nettstedet er åpent for bidrag fra alle samarbeidspartnere i SAMT-BU-prosjektet. Det finnes tre måter å bidra på, avhengig av hva slags endringer du skal gjøre og din tekniske bakgrunn:

| Metode | Passer for | Krever |
|--------|-----------|--------|
| [CMS-redigering](#alternativ-1--redigering-i-nettleseren-via-cms) | Fagpersoner og redaktører | GitHub-konto (gratis) |
| [GitHub-redigering](#alternativ-2--redigering-direkte-p-github) | Enkeltendringer, tekniske brukere | GitHub-konto + Markdown |
| [Lokal oppsett](#alternativ-3--lokal-oppsett-for-utviklere) | Strukturelle endringer, utviklere | Hugo + Git installert |

---

## Alternativ 1 – Redigering i nettleseren via CMS

**Dette er det anbefalte alternativet for de fleste bidragsytere.** Du redigerer innhold direkte i nettleseren i et visuelt redigeringsverktøy – ingen Markdown- eller Git-kunnskap nødvendig.

**Slik redigerer du en eksisterende side:**

1. Gå til siden du vil redigere på nettstedet
2. Klikk **«Endre»**-menyen øverst til høyre i headeren
3. Velg **«Denne siden»** – du sendes direkte til riktig side i CMS-editoren
4. Logg inn med GitHub-kontoen din (første gang: klikk «Login with GitHub»)
5. Gjør endringene dine i redigeringsfeltet
6. Klikk **«Lagre»** – endringen publiseres automatisk etter kort tid

**Slik lager du en ny side:**

1. Klikk **«Endre»** → **«Andre valg»** i headeren for å åpne CMS-portalen
2. Velg riktig samling i venstre panel
3. Klikk **«Ny»** og fyll inn tittel og innhold
4. Klikk **«Lagre»**

> **Merk:** Du trenger en GitHub-konto for å logge inn. Opprett én gratis på [github.com](https://github.com). Kontakt en administrator for å få skrivetilgang til riktig repo første gang.

---

## Alternativ 2 – Redigering direkte på GitHub

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

## Alternativ 3 – Lokal oppsett (for utviklere)

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
