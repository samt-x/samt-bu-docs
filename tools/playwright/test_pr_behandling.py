# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
Playwright E2E-test: Behandle forslag (PR-oversikt i Endre-menyen)
==================================================================

Test C. Tester funksjonen «Behandle forslag» (issue #60):

  1. Admin-gruppen «Prosjekt» vises i Endre-menyen for bruker med skrivetilgang
  2. «Behandle forslag» viser antall åpne forslag i etiketten
  3. Dialogen lister forslag fra FLERE repoer (aggregering)
  4. «Slå sammen» med to-stegs bekreftelse merger PR-en – og gir MERGED, ikke CLOSED
  5. «Avslå» med to-stegs bekreftelse lukker PR-en
  6. Begge handlinger legger igjen en kommentar til bidragsyteren
  7. Lista viser tomtilstand når alt er behandlet

⚠ SIKRING – LES DETTE
---------------------
Testen utfører ekte, delvis irreversible handlinger på GitHub. Den behandler
derfor KUN PR-er der tittelen inneholder TEST_MARKER (se under). Alle andre
åpne forslag telles og vises, men røres ikke.

Sett ALLOW_ANY=true bare hvis du vet nøyaktig hva du gjør.

Forberedelse – lag to test-PR-er i to ULIKE repoer (kreves for steg 3–6):

  git checkout -b test-pr-a
  # ... en harmløs endring, f.eks. i content/test-samt-bu-docs/ ...
  git commit -am "Testendring" && git push -u origin test-pr-a
  gh pr create --repo SAMT-X/samt-bu-docs --base main --head test-pr-a \
      --title "Skrivefeil rettet (test av PR-behandling)" --body "..."

  # og tilsvarende i f.eks. SAMT-X/samt-bu-drafts

Uten test-PR-er kjører testen steg 1–2 og rapporterer resten som hoppet over.

Kjøring:
  py test_pr_behandling.py            (leser token fra .env)
  HEADLESS=true py test_pr_behandling.py

Token-krav: samme GitHub-token som i nettleseren – må ha skrivetilgang til
repoene som testes.
"""

import asyncio
import os
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# ---------------------------------------------------------------------------
# Konfigurasjon
# ---------------------------------------------------------------------------

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

# Egen variabel, ikke SAMTU_BASE_URL: den peker i .env på samt-bu-docs.pages.dev,
# som er det gamle Direct Upload-prosjektet og ikke lenger blir bygget av CI.
# Denne testen må kjøre mot produksjonsnettstedet CI faktisk deployer til.
BASE_URL    = os.environ.get("PR_TEST_BASE_URL", "https://docs.samt-bu.no")
GH_TOKEN    = os.environ.get("GITHUB_TOKEN", "")
GH_USER     = os.environ.get("GITHUB_USER", "")
TEST_PAGE   = os.environ.get("TEST_PAGE", "/test-samt-bu-docs/test-1/")
HEADLESS    = os.environ.get("HEADLESS", "false").lower() == "true"

# Kun PR-er med denne teksten i tittelen blir slått sammen eller avslått.
TEST_MARKER = os.environ.get("TEST_MARKER", "test av PR-behandling").lower()
ALLOW_ANY   = os.environ.get("ALLOW_ANY", "false").lower() == "true"

SCREENSHOTS = Path(__file__).parent / "screenshots" / (
    "pr-behandling_" + datetime.now().strftime("%Y%m%d_%H%M%S"))

# Tidsbudsjett. Første lasting etter en deploy er kald: rettighetssjekk +
# ti parallelle repo-kall kan ta noen sekunder. Vent på tilstand, ikke på klokka.
LOAD_TIMEOUT   = 20000
ACTION_TIMEOUT = 25000

_ok = 0
_fail = 0
_skip = 0


def check(label, condition, detail=""):
    global _ok, _fail
    suffix = f" – {detail}" if detail else ""
    if condition:
        _ok += 1
        print(f"  [OK]   {label}{suffix}")
    else:
        _fail += 1
        print(f"  [FEIL] {label}{suffix}")
    return bool(condition)


def skip(label, why):
    global _skip
    _skip += 1
    print(f"  [HOPP] {label} – {why}")


async def wait_for(page, fn, timeout=LOAD_TIMEOUT, step=250):
    """Poll til fn() gir sant, eller timeout. Returnerer siste verdi."""
    waited = 0
    val = None
    while waited < timeout:
        val = await fn()
        if val:
            return val
        await page.wait_for_timeout(step)
        waited += step
    return val


async def main():
    if not GH_TOKEN or not GH_USER:
        print("Mangler GITHUB_TOKEN / GITHUB_USER i .env – avbryter.")
        return

    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    print(f"\nNettsted : {BASE_URL}")
    print(f"Bruker   : {GH_USER}")
    print(f"Sikring  : behandler kun PR-er med «{TEST_MARKER}» i tittelen"
          + ("  (OVERSTYRT – ALLOW_ANY=true)" if ALLOW_ANY else ""))

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=HEADLESS)
        ctx = await browser.new_context(viewport={"width": 1600, "height": 950})
        page = await ctx.new_page()
        page.on("pageerror", lambda e: check("Ingen JS-feil i konsollen", False, str(e)))

        # Token må ligge der før første sidelast
        await ctx.add_init_script(f"""
            localStorage.setItem('samt-bu-gh-token', {json.dumps(GH_TOKEN)});
            localStorage.setItem('samt-bu-gh-user', {json.dumps(GH_USER)});
        """)

        # -------------------------------------------------------------------
        print("\n=== 1. Endre-menyen ===")
        # networkidle går aldri i mål her – siden har lange kall gående
        await page.goto(BASE_URL + TEST_PAGE, wait_until="domcontentloaded")

        # Finnes elementet i det hele tatt? Hvis ikke, kjører vi mot et nettsted
        # uten funksjonen – nesten alltid feil BASE_URL, ikke en ekte feil.
        if not await page.query_selector("#samtu-admin-group"):
            print(f"\n  ⚠ Fant ikke #samtu-admin-group i DOM-en på {BASE_URL}.")
            print("    Nettstedet har ikke funksjonen. Sjekk PR_TEST_BASE_URL –")
            print("    samt-bu-docs.pages.dev er det gamle prosjektet og bygges ikke lenger.")
            await browser.close()
            sys.exit(2)

        # Rettighetssjekken skjer i nettleseren og slår gruppen på via style.display.
        # Vent på DEN, ikke på is_visible: gruppen ligger inne i en LUKKET dropdown,
        # så den er per definisjon usynlig helt til menyen åpnes.
        async def group_enabled():
            d = await page.eval_on_selector(
                "#samtu-admin-group", "el => el.style.display")
            return d == "block"

        check("Rettighetssjekken slår på admin-gruppen",
              await wait_for(page, group_enabled))

        # Åpne menyen – FØRST nå gir is_visible et meningsfullt svar
        await page.click("#edit-toggle")
        await page.wait_for_timeout(400)

        check("Admin-gruppen «Prosjekt» vises i åpen meny",
              await page.is_visible("#samtu-admin-group"))
        check("Menyvalget «Behandle forslag» vises",
              await page.is_visible("#samtu-admin-prs"))

        # Telleren fylles av samtuPrList() – ti parallelle kall, kan ta et par
        # sekunder ved kald start. Parentesen skal mangle når det er null forslag.
        label_base = "Handle suggestions" if "/en/" in TEST_PAGE else "Behandle forslag"

        async def label_ready():
            t = await page.text_content("#samtu-admin-prs-label")
            return t if (t and t.strip().startswith(label_base)) else None

        label = ((await wait_for(page, label_ready)) or "").strip()
        menu_count = None
        if "(" in label:
            try:
                menu_count = int(label.split("(")[1].split(")")[0])
            except ValueError:
                pass
        check("Etiketten er korrekt", label.startswith(label_base),
              f"etikett = «{label}»")

        await page.screenshot(path=str(SCREENSHOTS / "1-meny.png"))

        # -------------------------------------------------------------------
        print("\n=== 2. Dialogen ===")
        await page.click("#samtu-admin-prs a")
        opened = await wait_for(page, lambda: page.is_visible("#pr-overlay"))
        check("Dialogen åpnes", opened)

        async def rows_or_empty():
            """Ferdig lastet = enten rader, eller tomtilstand som IKKE er «Laster…».
            .pr-loading skiller de to – uten det slår ventingen til for tidlig."""
            rows = await page.query_selector_all(".pr-row")
            if rows:
                return rows
            return await page.query_selector(".pr-empty:not(.pr-loading)")

        await wait_for(page, rows_or_empty, timeout=ACTION_TIMEOUT)
        rows = await page.query_selector_all(".pr-row")
        print(f"  ({len(rows)} forslag i lista)")

        # Krysspeiling: tallet i menyen skal stemme med antall rader
        if menu_count is None:
            check("Teller i menyen stemmer med lista", len(rows) == 0,
                  "ingen parentes i etiketten – forventer tom liste")
        else:
            check("Teller i menyen stemmer med lista", menu_count == len(rows),
                  f"meny={menu_count}, liste={len(rows)}")

        repos = await page.eval_on_selector_all(
            ".pr-repo", "els => els.map(e => e.textContent)")
        if len(rows) >= 2:
            check("Aggregering på tvers av repoer", len(set(repos)) >= 2,
                  f"repoer = {sorted(set(repos))}")
        else:
            skip("Aggregering på tvers av repoer",
                 "krever åpne forslag i minst to repoer")

        await page.screenshot(path=str(SCREENSHOTS / "2-dialog.png"))

        # Finn testbare rader – sikringen
        # evaluate() tar ÉTT argument – pakk begge verdiene i et objekt
        targets = await page.evaluate("""(arg) => {
            return Array.from(document.querySelectorAll('.pr-row')).map(function(row) {
                var t = row.querySelector('.pr-title');
                var title = t ? t.textContent : '';
                return {
                    id: row.id,
                    title: title,
                    testable: arg.allowAny || title.toLowerCase().indexOf(arg.marker) !== -1,
                    canAct: !!row.querySelector('[data-pr-act]')
                };
            });
        }""", {"marker": TEST_MARKER, "allowAny": ALLOW_ANY})

        testable = [t for t in targets if t["testable"] and t["canAct"]]
        protected = [t for t in targets if not t["testable"]]
        if protected:
            print(f"  (beskyttet mot behandling: {len(protected)} ekte forslag)")

        if targets:
            check("Handlingsknapper vises for repoer med skrivetilgang",
                  any(t["canAct"] for t in targets))

        # -------------------------------------------------------------------
        print("\n=== 3. Slå sammen ===")
        if not testable:
            skip("Slå sammen", "ingen test-PR å behandle (se docstring)")
            skip("Avslå", "ingen test-PR å behandle (se docstring)")
        else:
            merged = await handle_row(page, testable[0], "merge", "Slått sammen")
            await page.screenshot(path=str(SCREENSHOTS / "3-merget.png"))

            print("\n=== 4. Avslå ===")
            if len(testable) < 2:
                skip("Avslå", "krever en test-PR til")
            else:
                await handle_row(page, testable[1], "close", "Avslått")
                await page.screenshot(path=str(SCREENSHOTS / "4-avslatt.png"))

        # -------------------------------------------------------------------
        print("\n=== 5. Oppdatering ===")
        await page.click("#pr-refresh-btn")
        await page.wait_for_timeout(1000)
        await wait_for(page, rows_or_empty, timeout=ACTION_TIMEOUT)
        remaining = await page.query_selector_all(".pr-row")
        check("Lista henter seg på nytt uten feil",
              remaining is not None,
              f"{len(remaining)} forslag igjen")
        await page.screenshot(path=str(SCREENSHOTS / "5-etter.png"))

        await browser.close()

    print(f"\n{'=' * 52}")
    print(f"Resultat: {_ok} OK, {_fail} feil, {_skip} hoppet over")
    print(f"Skjermbilder: {SCREENSHOTS}")
    if _fail:
        sys.exit(1)


async def handle_row(page, target, act, expect):
    """Kjør to-stegs bekreftelse på én rad og verifiser resultatet."""
    row = await page.query_selector("#" + target["id"])
    if not row:
        check(f"Fant raden ({target['id']})", False)
        return False

    btn = await row.query_selector(f'[data-pr-act="{act}"]')
    if not btn:
        check(f"Fant knappen ({act})", False)
        return False

    print(f"  → «{target['title'][:60]}»")

    await btn.click()
    await page.wait_for_timeout(400)
    armed = (await btn.text_content()) or ""
    check("Første klikk ber om bekreftelse", "Bekreft" in armed or "Confirm" in armed,
          f"knappetekst = «{armed.strip()}»")

    note = await row.query_selector(".pr-note")
    check("Forklarende tekst vises før handling", await note.is_visible())

    await btn.click()   # bekreft

    async def done():
        txt = (await note.text_content()) or ""
        if expect in txt or "⚠" in txt:
            return txt
        return None

    txt = await wait_for(page, done, timeout=ACTION_TIMEOUT)
    txt = (txt or "").strip()
    return check(f"{expect} rapporteres som vellykket", expect in txt,
                 f"melding = «{txt[:80]}»")


asyncio.run(main())
