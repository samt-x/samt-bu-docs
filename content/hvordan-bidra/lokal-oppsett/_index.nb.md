---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: "e26cb201-0841-46b2-8ac7-2ba3708edde6"
title: Lokalt oppsett
weight: 30

---
Dette alternativet gir deg et fullt lokalt arbeidsmiljø der du kan forhåndsvise alle endringer i nettleseren mens du skriver. Anbefalt for strukturelle endringer, nytt innhold i større omfang eller teknisk utvikling.

## Hva du trenger

| Verktøy | Versjon | Formål |
| --- | --- | --- |
| [Git](https://git-scm.com/) | Siste stabile | Versjonskontroll |
| [Hugo Extended](https://gohugo.io/) | 0.155.3 eller nyere | Nettstedsgenerator |
| [Go](https://go.dev/) | 1.21 eller nyere | Kreves av Hugo Modules |
| Teksteditor | – | [VS Code](https://code.visualstudio.com/) anbefales |

## Installasjon på Windows

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

## Installasjon på macOS

```bash
brew install git hugo go
```

## Installasjon på Linux (Ubuntu/Debian)

```bash
sudo apt install git golang
# Hugo Extended hentes fra GitHub Releases (apt-versjonen er ofte for gammel):
wget https://github.com/gohugoio/hugo/releases/download/v0.155.3/hugo_extended_0.155.3_linux-amd64.deb
sudo dpkg -i hugo_extended_0.155.3_linux-amd64.deb
```

## Innholdsstruktur – flere repos

SAMT-BU Docs er satt opp med **innholdsmoduler**: innhold fra ulike team og piloter ligger i egne GitHub-repoer og monteres automatisk inn i nettstedet ved publisering. Du trenger derfor ikke klone alle repoer for å se hele nettstedet – Hugo henter manglende moduler fra GitHub automatisk.

| Repo | Innhold | Montert under |
| --- | --- | --- |
| `samt-bu-docs` | Hoveddokumentasjon, konfigurasjon | *(rot)* |
| `samt-bu-pilot-1` | Pilot 1 | `pilotering/pilot-1/` |
| `samt-bu-pilot-2` | Pilot 2 | `pilotering/pilot-2/` |
| `samt-bu-pilot-3` | Pilot 3 | `pilotering/pilot-3/` |
| `samt-bu-pilot-4` | Pilot 4 | `pilotering/pilot-4/` |
| `team-architecture` | Overordnet arkitektur | `arkitektur/overordnet-arkitektur/` |
| `team-semantics` | Informasjonsarkitektur | `arkitektur/informasjonsarkitektur/` |
| `samt-bu-drafts` | Utkast og innspill | `utkast/` |
| `solution-samt-bu-docs` | Teknisk dokumentasjon | `prosjektleveranser/…` |

## Scenario A – Kun forhåndsvisning av hele nettstedet

Klon `samt-bu-docs` og start serveren. Hugo henter innholdet fra alle modulrepoer automatisk.

```bash
git clone --recurse-submodules https://github.com/SAMT-X/samt-bu-docs.git
cd samt-bu-docs
hugo server
```

Åpne <http://localhost:1313/> i nettleseren.

## Scenario B – Redigere innhold i ett bestemt repo

Ønsker du bare å redigere innhold i for eksempel `samt-bu-pilot-2`, trenger du kun å klone det repoet:

```bash
git clone https://github.com/SAMT-X/samt-bu-pilot-2.git
cd samt-bu-pilot-2
# rediger filer i content/
git add .
git commit -m "Beskrivelse av endringen"
git push
```

Nettstedet oppdateres automatisk på [docs.samt-bu.no](https://docs.samt-bu.no/) innen ca. ett minutt. Ingen lokal Hugo-server er nødvendig.

## Scenario C – Full lokal utvikling på tvers av alle repos

Vil du redigere innhold i flere moduler og se endringene live lokalt, klon alle repoer som søskenmapper og bruk det medfølgende hjelpe­scriptet:

```bash
# Klon samtlige repos side om side
git clone --recurse-submodules https://github.com/SAMT-X/samt-bu-docs.git
git clone https://github.com/SAMT-X/samt-bu-pilot-1.git
git clone https://github.com/SAMT-X/samt-bu-pilot-2.git
# ... osv. for de modulene du vil jobbe med

# Start lokal server (scriptet finner lokale kloner automatisk)
cd samt-bu-docs
tools/hugo-local.sh
```

Scriptet leser `hugo.toml`, oppdager hvilke moduler du har klonet lokalt, og starter Hugo med disse pekende på dine lokale filer. Moduler du ikke har klonet hentes fortsatt fra GitHub.

```
samt-bu-docs/            ← klon alltid denne
samt-bu-pilot-1/         ← klon de du vil redigere
samt-bu-pilot-2/
...
```

**Med utkast:**

```bash
tools/hugo-local.sh --drafts
```

## Skrive innhold

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

## Lagre og publisere endringer

```bash
git add content/sti/til/filen/_index.nb.md
git commit -m "Kort beskrivelse av hva du endret"
git push
```

GitHub Actions bygger og publiserer automatisk etter 1–2 minutter.

> **Uten skrivetilgang til repoet?** Opprett en *pull request* i stedet: `git checkout -b mitt-bidrag` → gjør endringer → `git push origin mitt-bidrag` → åpne PR på GitHub.

## Nyttige kommandoer

| Kommando | Beskrivelse |
| --- | --- |
| `tools/hugo-local.sh` | Start lokal server med automatisk modulerstatning |
| `tools/hugo-local.sh --drafts` | Inkluder også utkast (`draft: true`) |
| `hugo server` | Start lokal server (henter moduler fra GitHub) |
| `hugo` | Bygg til `public/` (sjekk for feil) |
| `git pull` | Hent siste endringer fra GitHub |
