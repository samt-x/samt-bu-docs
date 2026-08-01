# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
Playwright E2E-test: Bytt bruker (avatar-menyen)
=================================================

Test D. Sikrer at kontobytte gir GitHubs egen kontovelger:

  1. Avatar-menyen åpnes
  2. «Bytt bruker» logger ut lokalt og sender prompt=select_account
     (GitHubs nøytrale kontovelger – ingen skriving av brukernavn)
  3. Utlogging er KUN lokal (ingen /revoke – GitHub Apps mister hele
     godkjenningen ved revokering, som tvinger frem Authorize-skjermen
     ved hver innlogging) og viser melding med lenke til github.com/logout
  4. Pilen ved «Logg inn» gir kontovelgeren også fra UTLOGGET tilstand

Bakgrunn: GitHub bytter aldri konto av seg selv med aktiv sesjon, og
login=<navn> ga bare et «suggested»-banner med feil konto som standard.
prompt=select_account er GitHubs dokumenterte kontovelger. Testen finnes
for at mekanismen ikke skal forsvinne igjen (det skjedde i a38f7fb).

TRYGG Å KJØRE: testen fullfører aldri en innlogging, og /revoke-kallet fanges
opp lokalt (page.route) i stedet for å slippes ut – ingenting trekkes tilbake
på ekte. Kan kjøres så ofte du vil.

Kjøring:
  py test_bytt_bruker.py
  HEADLESS=true py test_bytt_bruker.py
"""

import asyncio
import os
import json
import time
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

        # Unik cache-buster: CDN-en henger etter en deploy i et par minutter, og
        # en gjenbrukt ?cb-verdi serverer den gamle siden på nytt. Det ser ut som
        # en ekte feil og har lurt oss flere ganger.
        await page.goto(BASE_URL + TEST_PAGE + "?cb=" + str(int(time.time())),
                        wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        if not await page.query_selector("#samt-bu-login-caret"):
            print(f"  ⚠ Fant ikke #samt-bu-login-caret på {BASE_URL}.")
            print("    Nettstedet mangler funksjonen – sjekk PR_TEST_BASE_URL,")
            print("    eller vent litt: CDN-en henger etter en deploy i et par minutter.")
            await browser.close()
            sys.exit(2)

        print("=== 1. Avatar-menyen ===")
        await page.click("#samt-bu-user-avatar")
        await page.wait_for_timeout(300)
        check("Avatar-menyen åpnes", await page.is_visible("#samt-bu-avatar-menu"))
        check("«Bytt bruker» finnes i menyen",
              await page.is_visible("#samt-bu-switch-row"))

        print("\n=== 2. «Bytt bruker» → GitHubs kontovelger ===")
        popup_url = {"v": None}

        async def on_popup(pg):
            popup_url["v"] = pg.url
            try:
                await pg.close()      # aldri fullfør innloggingen
            except Exception:
                pass

        page.on("popup", lambda pg: asyncio.create_task(on_popup(pg)))

        # Sikkerhetsnett: skulle /revoke noen gang gjeninnføres i utloggingen,
        # fanges kallet her i stedet for å slippes ut – og steg 3 slår alarm.
        revoke_req = {"body": None}

        async def handle_revoke(route):
            revoke_req["body"] = route.request.post_data
            await route.fulfill(status=200, content_type="application/json",
                                body='{"revoked":true}')

        await page.route("**/revoke", handle_revoke)

        await page.click("#samt-bu-switch-btn")
        await page.wait_for_timeout(3000)

        u = popup_url["v"] or ""
        # Popup fanges enten hos workeren (select=true) eller etter redirect
        # videre til GitHub (prompt=select_account) – begge beviser mekanismen.
        check("Kontovelgeren etterspørres (select_account)",
              ("select_account" in u) or ("select=true" in u), u[:95])
        check("Ingen login=-forslag (nøytral velger)", "login=" not in u)
        await page.screenshot(path=str(SCREENSHOTS / "1-bytt-bruker.png"))

        print("\n=== 3. Utlogging: revoke-kall + melding ===")
        # «Bytt bruker» logger allerede ut lokalt før popup-en åpnes, så avataren
        # er borte nå. Last siden på nytt – init-skriptet setter tokenet tilbake –
        # slik at vi tester utloggingen fra en ekte innlogget tilstand.
        await page.goto(BASE_URL + TEST_PAGE + "?cb=" + str(int(time.time())),
                        wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        check("Innlogget tilstand gjenopprettet før utloggingstesten",
              await page.is_visible("#samt-bu-user-avatar"))

        revoke_req["body"] = None   # ruten fra steg 2 er fortsatt aktiv

        await page.click("#samt-bu-user-avatar")
        await page.wait_for_timeout(250)
        await page.click("#samt-bu-logout-btn")
        await page.wait_for_timeout(700)

        check("Tokenet er fjernet lokalt",
              (await page.evaluate("localStorage.getItem('samt-bu-gh-token')")) is None)
        check("«Logg inn»-knappen er tilbake", await page.is_visible("#samt-bu-login-btn"))
        # GitHub Apps: revokering ⇒ Authorize-skjerm ved hver innlogging
        # (empirisk verifisert 2026-08-01). Utlogging skal derfor være KUN lokal.
        check("/revoke kalles IKKE (lokal utlogging)",
              revoke_req["body"] is None,
              "revokering ville tvunget frem Authorize-skjermen hver gang")

        shown = check("Melding vises etter utlogging",
                      await page.is_visible("#samt-bu-logout-notice"))
        if shown:
            txt = ((await page.text_content("#samt-bu-logout-notice")) or "").strip()
            check("Forklarer at neste innlogging bruker samme konto",
                  ("samme GitHub-konto" in txt) or ("same GitHub account" in txt),
                  txt[:60] + "…")
            check("Peker på pilen ved «Logg inn» for kontobytte",
                  ("pilen ved" in txt) or ("arrow next to" in txt))
            check("Tilbyr lenke til github.com/logout",
                  (await page.get_attribute("#samt-bu-logout-notice a", "href"))
                  == "https://github.com/logout")
        await page.screenshot(path=str(SCREENSHOTS / "3-utlogging.png"))

        print("\n=== 4. Utlogget: kontovelger via pilen ved «Logg inn» ===")
        # «Bytt bruker» finnes bare i avatar-menyen (krever innlogging). Pilen er
        # den ENESTE veien til kontovalg fra utlogget tilstand.
        check("Pilen ved «Logg inn» vises når man er utlogget",
              await page.is_visible("#samt-bu-login-caret"))

        popup_url["v"] = None          # popup-lytteren fra steg 2 er fortsatt aktiv
        await page.click("#samt-bu-login-caret")
        await page.wait_for_timeout(3000)
        u2 = popup_url["v"] or ""
        check("Pilen gir kontovelgeren (select_account)",
              ("select_account" in u2) or ("select=true" in u2), u2[:95])
        await page.screenshot(path=str(SCREENSHOTS / "4-kontovelger.png"))

        await browser.close()

    print(f"\n{'=' * 52}")
    print(f"Resultat: {_ok} OK, {_fail} feil")
    print(f"Skjermbilder: {SCREENSHOTS}")
    if _fail:
        sys.exit(1)


asyncio.run(main())
