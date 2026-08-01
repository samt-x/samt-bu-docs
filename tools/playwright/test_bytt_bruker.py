# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
Playwright E2E-test: Bytt bruker (avatar-menyen)
=================================================

Test D. Sikrer at kontobytte faktisk ber GitHub om en ANNEN konto:

  1. Avatar-menyen åpnes
  2. Brukernavnskjemaet er skjult til «Bytt bruker» klikkes
  3. Ugyldig brukernavn avvises med synlig melding
     (fanger regresjon av line-height:0-arven fra #samt-bu-avatar-wrap)
  4. Gyldig brukernavn sender login=<navn> på authorize-URL-en
  5. GitHub svarer med å sende brukeren til innloggingsskjemaet
  6. force=true brukes ikke når brukernavn er oppgitt

Bakgrunn: a38f7fb fjernet inputfeltet i troen på at GitHubs egen kontobytter
holdt. Det gjør den ikke – med aktiv github.com-sesjon og godkjent app får du
samme bruker tilbake. login=<brukernavn> er den dokumenterte måten å be om en
bestemt konto. Denne testen finnes for at den ikke skal forsvinne igjen.

TRYGG Å KJØRE: testen fullfører aldri en innlogging. Den leser bare URL-en
popup-vinduet sendes til, og lukker det. Ingenting endres, verken lokalt eller
på GitHub. Kan kjøres så ofte du vil.

Kjøring:
  py test_bytt_bruker.py
  HEADLESS=true py test_bytt_bruker.py
"""

import asyncio
import os
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

# Som Test C: egen variabel. SAMTU_BASE_URL/SAMTBU_BASE_URL peker i .env på
# samt-bu-docs.pages.dev, som ikke lenger bygges av CI.
BASE_URL  = os.environ.get("PR_TEST_BASE_URL", "https://docs.samt-bu.no")
GH_TOKEN  = os.environ.get("GITHUB_TOKEN", "")
GH_USER   = os.environ.get("GITHUB_USER", "")
TEST_PAGE = os.environ.get("TEST_PAGE", "/test-samt-bu-docs/test-1/")
HEADLESS  = os.environ.get("HEADLESS", "false").lower() == "true"

# Navnet trenger ikke finnes på GitHub – vi fullfører aldri innloggingen.
TARGET_USER = os.environ.get("SWITCH_TO_USER", "testbruker-uten-tilgang")

SCREENSHOTS = Path(__file__).parent / "screenshots" / (
    "bytt-bruker_" + datetime.now().strftime("%Y%m%d_%H%M%S"))

_ok = 0
_fail = 0


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


async def main():
    if not GH_TOKEN or not GH_USER:
        print("Mangler GITHUB_TOKEN / GITHUB_USER i .env – avbryter.")
        return

    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    print(f"\nNettsted   : {BASE_URL}")
    print(f"Bruker     : {GH_USER}")
    print(f"Bytter til : {TARGET_USER}  (innloggingen fullføres aldri)")
    print()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=HEADLESS)
        ctx = await browser.new_context(viewport={"width": 1600, "height": 950})
        page = await ctx.new_page()
        page.on("pageerror", lambda e: check("Ingen JS-feil i konsollen", False, str(e)))

        # Avatar må være satt, ellers vises «Logg inn»-knappen i stedet for menyen
        await ctx.add_init_script(f"""
            localStorage.setItem('samt-bu-gh-token', {json.dumps(GH_TOKEN)});
            localStorage.setItem('samt-bu-gh-user', {json.dumps(GH_USER)});
            localStorage.setItem('samt-bu-gh-avatar',
                'https://avatars.githubusercontent.com/u/1?v=4');
        """)

        await page.goto(BASE_URL + TEST_PAGE, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        if not await page.query_selector("#samt-bu-switch-form-row"):
            print(f"  ⚠ Fant ikke #samt-bu-switch-form-row på {BASE_URL}.")
            print("    Nettstedet mangler funksjonen – sjekk PR_TEST_BASE_URL,")
            print("    eller vent litt: CDN-en henger etter en deploy i et par minutter.")
            await browser.close()
            sys.exit(2)

        print("=== 1. Avatar-menyen ===")
        await page.click("#samt-bu-user-avatar")
        await page.wait_for_timeout(300)
        check("Avatar-menyen åpnes", await page.is_visible("#samt-bu-avatar-menu"))
        check("Skjemaet er skjult i utgangspunktet",
              not await page.is_visible("#samt-bu-switch-form-row"))

        print("\n=== 2. «Bytt bruker» åpner skjemaet ===")
        await page.click("#samt-bu-switch-btn")
        await page.wait_for_timeout(300)
        check("Brukernavnfeltet vises", await page.is_visible("#samt-bu-switch-form-row"))
        check("Lenken skjules mens skjemaet er åpent",
              not await page.is_visible("#samt-bu-switch-row"))
        await page.screenshot(path=str(SCREENSHOTS / "1-skjema.png"))

        print("\n=== 3. Validering ===")
        await page.fill("#samt-bu-switch-input", "ikke gyldig!!")
        await page.click("#samt-bu-switch-confirm")
        await page.wait_for_timeout(300)
        # is_visible fanger line-height:0-regresjonen: teksten finnes, men
        # elementet får null høyde og er reelt sett usynlig for brukeren.
        check("Ugyldig brukernavn avvises synlig",
              await page.is_visible("#samt-bu-switch-msg"),
              ((await page.text_content("#samt-bu-switch-msg")) or "").strip())
        await page.screenshot(path=str(SCREENSHOTS / "2-validering.png"))

        print("\n=== 4. Gyldig brukernavn → authorize-URL ===")
        popup_url = {"v": None}

        async def on_popup(pg):
            popup_url["v"] = pg.url
            try:
                await pg.close()      # aldri fullfør innloggingen
            except Exception:
                pass

        page.on("popup", lambda pg: asyncio.create_task(on_popup(pg)))

        await page.fill("#samt-bu-switch-input", TARGET_USER)
        await page.click("#samt-bu-switch-confirm")
        await page.wait_for_timeout(3000)

        u = popup_url["v"] or ""
        # Workeren svarer 302, så popup-en rekker som regel videre til GitHub
        # før vi leser URL-en. Begge stasjonene er riktige.
        check("Popup går til worker eller videre til GitHub",
              ("auth.samt-bu.no/auth" in u) or ("github.com/login" in u), u[:95])
        check("login=<brukernavn> er med", ("login=" + TARGET_USER) in u)
        check("GitHub sender til innloggingsskjema for kontoen",
              "github.com/login?" in u,
              "GitHub omdirigerte selv dit – dette er hele poenget")
        check("force=true brukes ikke når brukernavn er oppgitt", "force=true" not in u)

        await browser.close()

    print(f"\n{'=' * 52}")
    print(f"Resultat: {_ok} OK, {_fail} feil")
    print(f"Skjermbilder: {SCREENSHOTS}")
    if _fail:
        sys.exit(1)


asyncio.run(main())
