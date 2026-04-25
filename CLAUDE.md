# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Hva er dette?

**SAMT-BU Docs** – et statisk Hugo-basert dokumentasjonsnettsted for prosjektet SAMT-BU
(Sammenhengende tjenester for barn og unge). Én av flere dokumentasjonskanaler i prosjektet.
Publiseres til Cloudflare Pages på `https://docs.samt-bu.no/`.

## Teknisk oppsett

- **Rammeverk:** Hugo (Go-basert statisk nettstedsgenerator)
- **Tema:** `hugo-theme-samt-bu` (git submodule fra `github.com/samt-x/hugo-theme-samt-bu`, basert på Docdock/Altinn-tema)
  - Initialiseres ved kloning: `git submodule update --init --recursive`
  - Go-modul (`go.mod`/`go.sum`) styrer også tema-avhengigheten
- **Konfigurasjon:** `hugo.toml` (baseURL, språk, tema, outputs, editURL)
- **Språk:** Tospråklig – norsk bokmål (standard) og engelsk. Innhold i `_index.nb.md` / `_index.en.md`
- **Søk:** Lunr.js med Horsey.js autocomplete (`static/js/search.js`), generert fra Hugo JSON-output
- **Git-info:** `enableGitInfo = true` – sist-endret-datoer hentes fra commit-historikk

### Bygge og forhåndsvise

```bash
hugo server   # Lokal forhåndsvisning på http://localhost:1313/samt-bu-docs/
hugo          # Bygg til public/
hugo -D       # Bygg inkludert utkast (draft: true)

# Produksjonsbygg (brukes av CI)
hugo --gc --minify --baseURL "https://docs.samt-bu.no/"
```

CI/CD: GitHub Actions (`.github/workflows/hugo.yml`) bygger og deployer automatisk ved push til `main`. Hugo-versjon i CI: **0.155.3 extended**.

## Filstruktur – det viktigste

```
hugo.toml                          # Hugo-konfigurasjon (baseURL, språk, tema)
content/                           # Alt innhold (Markdown med YAML frontmatter)
  om/                              # «Om SAMT-BU» – intro-seksjon (weight 1)
    om-samt-bu/                    # Om prosjektet SAMT-BU (weight 1)
    om-dette-nettstedet/           # Om dette nettstedet (weight 2)
    hvordan-bidra/                 # Hvordan bidra (weight 3) – tre målgrupper: CMS, GitHub, lokal
  behov/                           # Behov (weight 10)
    use-cases/                     # 20 nummererte use cases (01–20)
    annet/                         # Annet (foreløpig)
  pilotering/                      # Piloter (weight 20)
    pilot-1/                       # 6 undermapper: overordnet-arkitektur, loesningsarkitektur, informasjonsarkitektur, juss, brukerreiser, annet
  arkitektur/                      # Arkitektur (weight 30)
    maalbildet/                    # Målbilde (weight 1)
    veikart/                       # Veikart (weight 2)
    informasjonsarkitektur/        # Informasjonsarkitektur (weight 30, tidligere egen toppnivå-seksjon)
  loesninger/                      # Løsninger (weight 40)
    cms-loesninger/                # CMS-løsninger (weight 10)
      samt-bu-docs/                # SAMT-BU Docs – teknisk dokumentasjon og administrasjonsveiledning
  rammeverk/                       # Rammeverk (weight 50)
    metodikk/                      # Metodikk (weight 30)
    juss/                          # Juss (weight 40)
    styring/                       # Styring (weight 50)
    begrepsapparat/                # Begrepsapparat (weight 10)
    standarder/                    # Standarder (weight 20)
  innsikt/                         # Felles innsikt – lokal placeholder (weight 70)
  teams/                           # Teams (weight 80) – lokalt seksjonshode
    team-architecture/             # ← montert fra Hugo Module team-architecture
    team-semantics/                # ← montert fra Hugo Module team-semantics
  utkast/                          # Utkast og innspill (weight 90) – ← montert fra Hugo Module samt-bu-drafts
themes/hugo-theme-samt-bu/         # ⭐ Git submodule – all presentasjonslogikk ligger her
  layouts/partials/
    custom-head.html               # ⭐ HOVEDDELEN – all tilpasset CSS
    topbar.html                    # Header-bar med logo, tittel, Rediger/Edit-knapp
    header.html                    # HTML-skjelett: <head>, <body>, 3-kolonne wrapper
    menu.html                      # Venstre sidebar-navigasjon (hierarkisk meny)
    footer.html                    # Footer med prev/next-nav, GitHub-redigeringslenke, TOC
    footer-content.html            # Footer-innhold (misjonserklæring)
    custom-footer.html             # JS for tema-switcher, edit-switcher og språkvelger
    tema-switcher.html             # Innhold/Content-dropdown (10 seksjoner)
    edit-switcher.html             # Endre/Edit-dropdown (deep-link til Decap CMS)
    lang-switcher.html             # Språkvelger (flaggikoner nb/en)
    search.html                    # Søkefelt-integrasjon
    status-symbol.html             # Slår opp statussymbol fra .Params.status
  layouts/_default/list.html       # Override for listesider
  layouts/shortcodes/              # children.html, header.html, relref.html
static/
  images/SAMT-BU-logo.png          # Logo (vises invertert i header)
  images/nb.svg, en.svg            # Flaggikoner for språkvelger
  js/search.js                     # Lunr.js søkeimplementasjon
  edit/                            # Decap CMS – innholdsredigering
    index.html                     # Norsk portalside («English →»-lenke i header)
    en/index.html                  # Engelsk portalside («Norsk →»-lenke i header)
    docs-nb/, arkitektur-nb/, utkast-nb/     # Norske CMS-portaler (locales: [nb], locale: nb)
    docs-en/, arkitektur-en/, utkast-en/     # Engelske CMS-portaler (locales: [en])
.github/
  workflows/hugo.yml               # CI/CD: bygg og deploy til GitHub Pages
  workflows/ensure-uuids.yml       # ⭐ UUID-workflow: sikrer id-felt i all frontmatter automatisk
  scripts/ensure-uuids.py          # Python-skript brukt av UUID-workflow
  scripts/inject-lastmod.py        # Injiserer lastmod i modulinnhold fra git-historikk (kjøres i CI før hugo)
cloudflare-worker/
  oauth-worker.js                  # GitHub OAuth-proxy (deployet på Cloudflare Workers)
i18n/nb.toml, en.toml              # Oversettelser (navSwitcher-etiketter, seksjonstitler, «Sist endret»)
```

## Decap CMS – innholdsredigering

- **OAuth-proxy:** Cloudflare Worker `https://auth.samt-bu.no`
- **Header-dropdown («Endre»/«Edit»):** Erstatter gammel statisk knapp. Implementert i `edit-switcher.html`.
  - «Denne siden»/«This page» → deep-link til gjeldende side i riktig portal
  - «Andre valg»/«Other options» → CMS-oversikt (`/edit/` eller `/edit/en/`)
  - **Rutinglogikk (tre grener)** basert på `$dir = path.Dir .File.Path`:
    - `hasPrefix $dir "teams/"` → arkitektur-portal, collection `arkitektur`
    - `eq/hasPrefix $dir "utkast"` → utkast-portal, collection `utkast`
    - `eq/hasPrefix $dir "loesninger/cms-loesninger/samt-bu-docs"` → loesninger-portal, collection `loesninger`
    - alt annet → docs-portal, collection `docs`
  - **Entry-slug:** Full relativ sti inkl. `/_index` (f.eks. `kommuneforlaget/_index`). Rot-sider i moduler bruker `_index` alene. Docs-rot forblir deaktivert (tom slug). URL: `<portal>#/collections/<collection>/entries/<slug>`
  - **Windows-fallgruve:** `.File.Path` bruker backslash – bruk alltid `path.Dir .File.Path` (normaliserer) fremfor rå `.File.Path` for hasPrefix-sjekker
- **Frontmatter-format:** YAML (`---`) – ikke TOML.
- **OBS:** CMS-sesjoner kan legge igjen testinnhold – sjekk `git diff` før push.

### Aktive CMS-portaler

| Mappe | Repo | Språk | Portalkorttittel | CMS-samlingsnavn |
|-------|------|-------|------------------|-----------------|
| `static/edit/docs-nb/` | `SAMT-X/samt-bu-docs` | nb | Gjeldende dokumentasjon | Sider |
| `static/edit/docs-en/` | `SAMT-X/samt-bu-docs` | en | Current documentation | Pages |
| `static/edit/arkitektur-nb/` | `SAMT-X/team-architecture` | nb | Team arkitektur | Team arkitektur |
| `static/edit/arkitektur-en/` | `SAMT-X/team-architecture` | en | Team architecture | Team architecture |
| `static/edit/utkast-nb/` | `SAMT-X/samt-bu-drafts` | nb | Innspill og utkast | Innspill og utkast |
| `static/edit/utkast-en/` | `SAMT-X/samt-bu-drafts` | en | Inputs and drafts | Inputs and drafts |
| `static/edit/loesninger-nb/` | `SAMT-X/solution-samt-bu-docs` | nb | Løsningsdokumentasjon | Løsningsdokumentasjon |
| `static/edit/loesninger-en/` | `SAMT-X/solution-samt-bu-docs` | en | Solution documentation | Solution documentation |

**Kritisk:** Hvert Hugo-modulrepo som monterer innhold **må ha sin egen CMS-portal** pekende på det repoet. Feilruting til `docs`-portalen → CMS viser tomme felter uten feilmelding (filene finnes ikke i `samt-bu-docs`-repoet).

**NB-portaler har i tillegg:**
- `locale: nb` i `config.yml`
- Inline JS-lokale i `index.html` som oversetter `«Collections» → «Samlinger»` og `«New» → «Ny»`
- Risiko ved Decap-oppgradering dokumentert i [issue #66](https://github.com/SAMT-X/samt-bu-docs/issues/66)

**Alle portaler har:**
- `sortable_fields: ['weight', 'title']` – sorterer etter Hugo `weight` (matcher sidebar-rekkefølge)

### Legge til ny CMS-portal

1. Opprett mappe `static/edit/<seksjon>-nb/` med:
   - `index.html` (← Portal-lenke → `../` + JS-lokale-blokk for NB)
   - `config.yml` (`locales: [nb]`, `locale: nb`, `repo: SAMT-X/<repo>`, `sortable_fields: ['weight', 'title']`)
2. Legg til kort i `static/edit/index.html` og `static/edit/en/index.html`
3. Gjenta for `-en/` uten `locale: nb` og uten JS-lokale, lenke → `../en/`
4. Legg til nytt grein i `edit-switcher.html` (i temaet) *før* `{{ else }}`-blokken
5. Commit temaendring → push → oppdater submodule-peker i samt-bu-docs

## Innholdskonvensjoner

- Alle seksjoner har `_index.nb.md` og `_index.en.md`
- Frontmatter-felter: `id` (UUID, delt mellom nb/en), `weight` (sorteringsrekkefølge), `status`, `draft: true` for upublisert innhold
- **`id`-felt:** UUID v4, samme verdi i `_index.nb.md` og `_index.en.md` for samme side. Aldri endres.
  Håndteres automatisk av GitHub Actions-workflow (`.github/workflows/ensure-uuids.yml`) i alle tre repoer –
  aldri sett manuelt. `widget: hidden` i Decap CMS (skjult fra redaktøren).
- `editURL` i `hugo.toml` genererer "Rediger på GitHub"-lenker: `https://github.com/SAMT-X/samt-bu-docs/edit/main/content/`
- **Commit-meldinger skrives på norsk** (se git-historikken for stil)

### Statussymboler for use cases

Symbolet genereres **automatisk** av `status-symbol.html` fra `status`-feltet – **ikke** lagret i `linkTitle`.
Redaktøren trenger kun endre `status:`-feltet:

| Symbol | NB-verdi | EN-verdi |
|--------|----------|----------|
| ◍ | Ny | New |
| ◔ | Tidlig utkast | Early draft |
| ◐ | Pågår | In progress |
| ◕ | Til QA | For QA |
| ⏺ | Godkjent | Approved |
| ⨂ | Avbrutt | Cancelled |

- NB-filer bruker norske verdier, EN-filer bruker engelske verdier.
- `status-symbol.html` håndterer begge språk.
- Kun use case-filer (01–20 under `behov/use-cases/`) har status satt; øvrige sider har blank status.
- Alle use case-filer har en kommentarblokk i frontmatter som viser gyldige verdier.

## Arkitekturbeslutninger

### 3-kolonne layout med uavhengig scroll

Den viktigste arkitekturbeslutningen. Implementert i `custom-head.html` (linje ~268+):

- **Viewport er låst** (`html, body { height: 100%; overflow: hidden }`) – ingen sidescroll
- **Flexbox-kolonnemodell:** header og footer har fast plass, containeren mellom fyller resten
- **Tre kolonner scroller uavhengig:**
  1. **Venstre (#sidebar):** 20% bredde, maks 260px – navigasjonsmeny
  2. **Midten (#body):** flex 1 – innholdsområde
  3. **Høyre (#page-toc):** 18% bredde, maks 240px – innholdsfortegnelse (TOC)
- **Scrollbarer er skjult** (`scrollbar-width: none` + `::-webkit-scrollbar { display: none }`)
- **Scroll-fade:** Gradient-fade plassert ved visuell bunn av sidebar og TOC viser at det er mer innhold under (JS i `footer.html`)
- **Scroll-spy i TOC:** Aktiv seksjon markeres med bold i TOC-kolonnen mens bruker scroller
- **Mobil:** TOC skjules, single-column layout, vanlig sidescroll
- **Collapsible sidebars:** Toggle-knapper i heading-rad (`#toggle-left` / `#toggle-right`) kollapser kolonnen til 0px. Restore-tabs (`#restore-left` / `#restore-right`) er `position: fixed` direkte i `<body>` (i `header.html`). Tilstand lagres i localStorage.

### Header (det mørkeblå feltet)

- Tema-CSS setter `height: 100px; padding-top: 32px` ved ≥768px
- Overstyrt i `custom-head.html` til `height: auto; padding: 13px 0` (~66px total)
- Innholdet er vertikalt midtstilt med `display: flex; align-items: center` (inline i `topbar.html`)
- Inneholder: logo, tittel, tema-switcher, søk, språkvelger, Endre/Edit-dropdown

### Grått mellomrom (header → kolonner)

- Bootstrap-klasser `pt-md-3 pt-lg-5` på containeren overstyres til halve verdier
- `padding-top: 0.5rem` (768px+) og `1.5rem` (992px+)

### CSS-lagmodell

Tre lag der sistnevnte vinner: `designsystem.css` → `theme.css` → `custom-head.html`

### Container-bredde

Utvidet fra standard Bootstrap: `width: 95vw; max-width: 1400px` ved ≥1200px, `1600px` ved ≥1600px

### Innhold/Content-dropdown (`layouts/partials/tema-switcher.html`)

Dropdown i headeren for å navigere direkte til en av de 10 seksjonene.

- **Etikett:** «Innhold» (nb) / «Content» (en) – styrt av i18n-nøkkel `navSwitcherLabel`
- **Aktiv-deteksjon:** `findRE (printf "/%s/" .id) .RelPermalink` – matcher hele URL-segment
- **Titler:** Oversatt via i18n med `.id` som nøkkel, `.title` som norsk fallback
- **Konfigurasjon:** `[[params.navSwitcher]]` i `hugo.toml` – id, title, url, icon
- **Legg til ny seksjon:** Ny `[[params.navSwitcher]]`-blokk i `hugo.toml` + i18n-nøkkel i `nb.toml`/`en.toml`

### Typografi

- Brødtekst: 16px, Helvetica Neue / Helvetica / Arial
- Sidebar: 15px
- TOC: 13px, 2px solid venstre kantlinje
- Kulepunkter: Tett avstand (4px margin), hierarkisk innrykk (disc → circle → square)

## Nåværende status

### Hva er ferdig

- Hugo-oppsett med tema (submodule), tospråklig konfigurasjon, søk
- 3-kolonne layout med uavhengig scroll
- Header med logo, tittel, Innhold/Content-dropdown, søk, språkvelger, Endre/Edit-dropdown (deep-link til Decap)
- Scroll-fade, scroll-spy i TOC, collapsible sidebars med localStorage-persistens
- Barn-liste på seksjonssider (midt- og høyrekolonne)
- «Om SAMT-BU» som første seksjon med tre underkapitler (Om prosjektet, Om dette nettstedet, Hvordan bidra)
- 10 seksjoner i flat struktur direkte under `content/`
- Hugo Module-integrasjon: team-architecture, team-semantics og samt-bu-drafts montert
- Nettsted omdøpt til «SAMT-BU Docs», `loesning/` omdøpt til `loesninger/`
- Ny dokumentasjonsstruktur: `loesninger/cms-loesninger/samt-bu-docs/` (teknisk dok. + administrasjonsveiledning)
- 20 use cases under Behov (inkl. Kommuneforlaget brukstilfelle-analyse)
- Decap CMS med norsk og engelsk portal, tospråklig redigering bekreftet
- «Denne siden»/«This page» deep-link i Endre-dropdown for alle sider inkl. modul-sider (teams/team-architecture, utkast)
- UUID-workflow (`.github/workflows/ensure-uuids.yml`) i alle tre repoer – sikrer id-felt i frontmatter automatisk
- `widget: hidden` for id-felt i alle 6 Decap-portaler – UUID er usynlig for redaktøren
- «Sist endret»-tidsstempler for modulinnhold via `inject-lastmod.py` + `HUGO_MODULE_REPLACEMENTS` i CI
- Sidebar-ikon fikset: aktiv seksjon viser sort-down (åpen) i stedet for caret-right (lukket)

### Hva gjenstår / pågår

- Fylle inn faktisk innhold i alle seksjoner
- Finjustere responsiv design for mobil/tablet

## Hugo Modules – innholdsmoduler

Innhold fra eksterne repoer monteres inn via Hugo Module-systemet (`go.mod` + `hugo.toml`).

| Modul | Repo | Montert under | Tittel |
|-------|------|---------------|--------|
| `github.com/SAMT-X/team-architecture` | [team-architecture](https://github.com/SAMT-X/team-architecture) | `content/teams/team-architecture/` | Team arkitektur |
| `github.com/SAMT-X/team-semantics` | [team-semantics](https://github.com/SAMT-X/team-semantics) | `content/teams/team-semantics/` | Team semantikk |
| `github.com/SAMT-X/samt-bu-drafts` | [samt-bu-drafts](https://github.com/SAMT-X/samt-bu-drafts) | `content/utkast/` | Utkast og innspill |
| `github.com/SAMT-X/solution-samt-bu-docs` | [solution-samt-bu-docs](https://github.com/SAMT-X/solution-samt-bu-docs) | `content/loesninger/cms-loesninger/samt-bu-docs/` | SAMT-BU Docs (teknisk dok.) |

**Konfigurert i `hugo.toml`** under `[module] [[module.imports]]` med `source = "content"` og `target = "content/<sti>/"`.

**Oppdatere en modul** (etter push til modulrepoet):
```bash
hugo mod get github.com/SAMT-X/samt-bu-drafts@latest
hugo mod get github.com/SAMT-X/team-architecture@latest
```

**Legge til ny modul:**
1. Opprett repo, `hugo mod init github.com/SAMT-X/<navn>`, lag `content/_index.nb.md` + `_index.en.md`, push
2. Legg til `[[module.imports]]`-blokk i `hugo.toml`
3. Kjør `hugo mod get github.com/SAMT-X/<navn>@latest`
4. Verifiser med `hugo`, commit `hugo.toml` + `go.mod` + `go.sum`

**Repo-navnekonvensjon:**
- `samt-bu-`-prefiks = publisert innhold/produkt (montert i nettstedet)
- `team-`-prefiks = interne arbeidsrepoer for team

## CI-workflow – hugo.yml (utover standard)

`hugo.yml` gjør mer enn bare å bygge. Ekstra steg i `build`-jobben:

1. **Checkout modulrepoer med full historikk:**
   ```yaml
   - uses: actions/checkout@v4
     with:
       repository: SAMT-X/team-architecture
       path: .hugo-modules/team-architecture
       fetch-depth: 0
   ```
   (samme for `samt-bu-drafts`)

2. **Inject lastmod** (`.github/scripts/inject-lastmod.py`):
   Leser `git log -1 --format=%cI` for hver `.md`-fil i modulrepoene og skriver `lastmod: <ISO-tidsstempel>` inn i frontmatter i CI-workspace. **Ingen commit** – kun midlertidig endring før bygg.

3. **`HUGO_MODULE_REPLACEMENTS`** (env-var på Build-steget):
   ```
   github.com/SAMT-X/team-architecture -> ${{ github.workspace }}/.hugo-modules/team-architecture
   ```
   Gjør at Hugo bruker de lokale klonene (med injisert lastmod) i stedet for Go-modulcachen (zip uten historikk).

**Kjent begrensning:** Lokalt (`hugo server`) vises ingen `lastmod` for modulinnhold – Hugo bruker modulcachen. Kun produksjonsbygg (CI) har korrekte tidsstempler for modul-sider.

## Verktøy

- **GitHub CLI (`gh`):** Installert (`winget`), versjon 2.87.2. Autentisert mot GitHub.
  - Ikke i PATH i alle shell-kontekster – bruk full sti: `"/c/Program Files/GitHub CLI/gh.exe"`
  - Eksempel: `"/c/Program Files/GitHub CLI/gh.exe" repo rename nytt-navn --repo org/gammelt-navn`
  - **Slette repos krever ekstra scope:** Kjør `gh auth refresh -h github.com -s delete_repo` og fullfør nettleserflyt før sletting

## Viktige tips for ny sesjon

1. **All tilpasset CSS er i `themes/hugo-theme-samt-bu/layouts/partials/custom-head.html`** – dette er filen du oftest redigerer for layout/styling
2. **Layout-filer redigeres i temaet** (`themes/hugo-theme-samt-bu/`) – commit der, deretter oppdater submodule-peker i samt-bu-docs
3. **Tema-CSS-en har tre lag:** `designsystem.css` → `theme.css` → `custom-head.html` (sistnevnte vinner)
4. **Bygg med `hugo`** for å verifisere at endringer kompilerer uten feil
5. **Inline styles i `topbar.html`** – header-nav har mye inline CSS for flex-layout
6. **Commit-meldinger skrives på norsk** (se git-historikken for stil)
7. **Submodule-oppdatering:** etter commit i temaet, kjør `git add themes/hugo-theme-samt-bu && git commit` i samt-bu-docs
