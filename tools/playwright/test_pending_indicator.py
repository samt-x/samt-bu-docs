# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
Playwright E2E-test: Pending build-indikator
=============================================

Tester at pending-indikatoren:
  1. Vises med riktig count etter lagring
  2. Gjenopprettes etter sidenavigering
  3. Decrementerer én gang per ferdig bygg
  4. Forsvinner når count = 0

Genererer også dokumentasjons-screenshots i screenshots/

Kjøring:
  pip install playwright python-dotenv
  playwright install chromium
  GITHUB_TOKEN=<ditt-token> python test_pending_indicator.py

  Eller med .env-fil (se .env.example).

Token-krav: GitHub PAT med 'repo' og 'workflow'-scope (samme som du bruker i nettleseren).
"""

import asyncio
import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, BrowserContext

# ---------------------------------------------------------------------------
# Konfigurasjon
# ---------------------------------------------------------------------------

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

BASE_URL    = os.environ.get("SAMTU_BASE_URL", "https://samt-bu-docs.pages.dev")
GH_TOKEN    = os.environ.get("GITHUB_TOKEN", "")
GH_USER     = os.environ.get("GITHUB_USER", "")          # Ditt GitHub-brukernavn
TEST_PAGE   = os.environ.get("TEST_PAGE", "/test-samt-bu-docs/test-1/")   # Dedikert testside
HEADLESS    = os.environ.get("HEADLESS", "false").lower() == "true"
SLOW_MO     = int(os.environ.get("SLOW_MO", "400"))       # ms – lavere = raskere, 0 = maks hastighet

SCREENSHOTS = Path(__file__).parent / "screenshots" / datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------------------------------------------------------------------------
# Hjelpefunksjoner
# ---------------------------------------------------------------------------

async def screenshot(page: Page, name: str, highlight_selector: str = None):
    """Ta screenshot med valgfri element-highlight. Filnavn prefix angir rekkefølge."""
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    path = SCREENSHOTS / f"{name}.png"

    if highlight_selector:
        # Tegn rød ramme rundt elementet FØR screenshot
        await page.evaluate(f"""
            (sel) => {{
                const el = document.querySelector(sel);
                if (el) {{
                    el._origOutline = el.style.outline;
                    el._origZIndex  = el.style.zIndex;
                    el.style.outline = '3px solid #e63946';
                    el.style.zIndex  = '9999';
                }}
            }}
        """, highlight_selector)
        await page.screenshot(path=str(path), full_page=False)
        # Fjern highlight
        await page.evaluate(f"""
            (sel) => {{
                const el = document.querySelector(sel);
                if (el) {{
                    el.style.outline = el._origOutline || '';
                    el.style.zIndex  = el._origZIndex  || '';
                }}
            }}
        """, highlight_selector)
    else:
        await page.screenshot(path=str(path), full_page=False)

    print(f"  📸 {path.name}")
    return path


async def inject_credentials(page: Page):
    """Injiser GitHub-token og brukernavn i localStorage."""
    if not GH_TOKEN:
        print("⚠  GITHUB_TOKEN ikke satt – hopper over autentisering")
        return
    await page.evaluate(f"""
        localStorage.setItem('samt-bu-gh-token', {json.dumps(GH_TOKEN)});
        localStorage.setItem('samt-bu-gh-user', {json.dumps(GH_USER)});
    """)
    print(f"  🔑 Token injisert for bruker: {GH_USER or '(ikke satt)'}")


async def get_pending_state(page: Page) -> dict:
    """Les samtu-build-pending fra localStorage."""
    raw = await page.evaluate("localStorage.getItem('samtu-build-pending')")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw}


async def wait_for_indicator(page: Page, timeout_ms: int = 5000) -> bool:
    """Vent til #qe-job-indicator er synlig. Returnerer True ved suksess."""
    try:
        await page.wait_for_function(
            "document.getElementById('qe-job-indicator')?.style.display === 'flex'",
            timeout=timeout_ms
        )
        return True
    except Exception:
        return False


async def wait_for_indicator_hidden(page: Page, timeout_ms: int = 180000) -> bool:
    """Vent til #qe-job-indicator er skjult (bygg ferdig). Returnerer True ved suksess."""
    try:
        await page.wait_for_function(
            "!document.getElementById('qe-job-indicator') "
            "|| document.getElementById('qe-job-indicator').style.display === 'none' "
            "|| document.getElementById('qe-job-indicator').style.display === ''",
            timeout=timeout_ms
        )
        return True
    except Exception:
        return False


async def get_indicator_text(page: Page) -> str:
    """Hent synlig tekst i #qe-job-indicator."""
    return await page.evaluate(
        "document.getElementById('qe-job-indicator')?.innerText?.trim() || ''"
    )


# ---------------------------------------------------------------------------
# Teststeg
# ---------------------------------------------------------------------------

async def step_01_load_site(page: Page):
    print("\n[1/9] Laster nettstedet…")
    await page.goto(BASE_URL + TEST_PAGE, wait_until="networkidle")
    await screenshot(page, "01-startside")
    print(f"  ✓ Nettsted lastet: {BASE_URL + TEST_PAGE}")


async def step_02_inject_and_reload(page: Page):
    print("\n[2/9] Injiserer credentials og laster siden på nytt…")
    await inject_credentials(page)
    await page.reload(wait_until="networkidle")
    await screenshot(page, "02-etter-innlogging")


async def step_03_open_edit_menu(page: Page):
    print("\n[3/9] Åpner Endre-menyen…")
    edit_btn = page.locator("#edit-toggle")
    await edit_btn.wait_for(state="visible", timeout=5000)
    await edit_btn.click()
    await page.wait_for_timeout(400)
    # Vent til menyen er synlig og highlight «Rediger dette kapitlet»
    rediger_item = page.locator("#edit-menu a").filter(
        has_text=re.compile(r"Rediger dette kapitlet|Edit this chapter", re.IGNORECASE)
    ).first
    await rediger_item.wait_for(state="visible", timeout=5000)
    await screenshot(page, "03-endre-meny-apen", "#edit-menu")
    # Screenshot med highlight på valgt menyvalg
    await page.evaluate("""
        const el = Array.from(document.querySelectorAll('#edit-menu a'))
            .find(a => /Rediger dette kapitlet|Edit this chapter/i.test(a.textContent));
        if (el) { el._hl = el.style.background; el.style.background = '#ffe066'; }
    """)
    await screenshot(page, "03b-menyvalg-rediger-highlight")
    await page.evaluate("""
        const el = Array.from(document.querySelectorAll('#edit-menu a'))
            .find(a => /Rediger dette kapitlet|Edit this chapter/i.test(a.textContent));
        if (el) el.style.background = el._hl || '';
    """)
    print("  ✓ Endre-meny åpnet – «Rediger dette kapitlet» uthevet i screenshot")


async def step_04_open_edit_dialog(page: Page):
    print("\n[4/9] Åpner redigeringsdialog…")
    rediger = page.locator("#edit-menu a").filter(
        has_text=re.compile(r"Rediger dette kapitlet|Edit this chapter", re.IGNORECASE)
    ).first
    await rediger.wait_for(state="visible", timeout=5000)
    await rediger.click()
    await page.wait_for_selector("#qe-overlay", state="visible", timeout=10000)
    # Vent til tittelfelt er populert (frontmatter er lastet)
    await page.wait_for_function(
        "document.getElementById('qe-field-title')?.value?.length > 0",
        timeout=15000
    )
    await screenshot(page, "04-redigeringsdialog-apen", "#qe-meta-panel")
    print("  ✓ Redigeringsdialog åpnet og frontmatter lastet")


async def step_05_make_change(page: Page):
    print("\n[5/9] Endrer tittelen – synlig i venstremenyen etter bygg…")
    title_input = page.locator("#qe-field-title")
    await title_input.wait_for(state="visible", timeout=10000)
    current_title = await title_input.input_value()
    # Fjern eventuell gammel tidsstempel-suffix
    base_title = re.sub(r'\s*\(testet \d{2}:\d{2}:\d{2}\)$', '', current_title).strip()
    ts = datetime.now().strftime("%H:%M:%S")
    new_title = f"{base_title} (testet {ts})"
    await title_input.click(click_count=3)
    await title_input.fill(new_title)
    await screenshot(page, "05-tittel-endret", "#qe-meta-panel")
    print(f"  ✓ Tittel endret: «{current_title}» → «{new_title}»")


async def step_06_save_and_observe_indicator(page: Page):
    print("\n[6/9] Lagrer og observerer pending-indikator…")
    save_btn = page.locator("#qe-save-btn")
    await save_btn.click()

    # Vent på at status-tekst viser «Lagret»
    try:
        await page.wait_for_function(
            "document.getElementById('qe-status-text')?.textContent?.includes('Lagret') "
            "|| document.getElementById('qe-status-text')?.textContent?.includes('Saved')",
            timeout=30000
        )
        print("  ✓ Commit sendt")
    except Exception:
        print("  ⚠ Timeout – commit kanskje ikke sendt")

    await page.wait_for_timeout(500)
    await screenshot(page, "06-etter-lagring-dialog", "#qe-overlay")

    # Les pending-state
    state = await get_pending_state(page)
    print(f"  📦 Pending state: {state}")

    # Lukk dialog for å se indikatoren tydelig
    cancel_btn = page.locator("#qe-cancel-btn")
    await cancel_btn.click()
    await page.wait_for_selector("#qe-overlay", state="hidden", timeout=5000)

    # Vent til indikatoren vises
    visible = await wait_for_indicator(page)
    if visible:
        text = await get_indicator_text(page)
        print(f"  ✓ Indikator synlig: «{text}»")
        await screenshot(page, "06b-pending-indikator-synlig", "#qe-job-indicator")
    else:
        print("  ⚠ Indikator ikke synlig etter lagring")
        await screenshot(page, "06b-ingen-indikator")


async def step_07_navigate_away(page: Page):
    print("\n[7/9] Navigerer til annen side og sjekker at indikator gjenopprettes…")
    # Naviger til Test 2 – holder Test-kapitlet ekspandert i sidebar
    await page.goto(BASE_URL + "/test-samt-bu-docs/test-2/", wait_until="networkidle")
    await page.wait_for_timeout(800)  # Resume-kode kjøres etter 200ms

    current_url = page.url
    print(f"  → Navigerte til: {current_url}")

    # Sjekk at indikatoren er gjenopprettet
    visible = await wait_for_indicator(page, timeout_ms=4000)
    if visible:
        text = await get_indicator_text(page)
        state = await get_pending_state(page)
        print(f"  ✓ Indikator gjenopprettet etter navigering: «{text}»")
        print(f"  📦 State: {state}")
        await screenshot(page, "07-indikator-etter-navigering", "#qe-job-indicator")
    else:
        print("  ⚠ Indikator IKKE gjenopprettet etter navigering – feil!")
        await screenshot(page, "07-indikator-mangler-etter-navigering")


async def step_08_wait_for_build_and_countdown(page: Page):
    print("\n[8/9] Venter på bygg og observerer nedtelling (kan ta 1–3 min)…")
    print("  ⏳ Poller GitHub Actions – venter…")

    prev_state = await get_pending_state(page)
    prev_count = prev_state.get("count", 0)

    # Ta screenshot hvert 15. sek for å fange mellomtilstander
    for i in range(12):  # maks 3 min
        await page.wait_for_timeout(15000)
        state   = await get_pending_state(page)
        count   = state.get("count", 0)
        ind_txt = await get_indicator_text(page)

        print(f"  ⏱ {(i+1)*15}s – count={count}, indikator: «{ind_txt}»")

        if count < prev_count or count == 0:
            print(f"  ✓ Count decrementert: {prev_count} → {count}")
            await screenshot(page, f"08-bygg-ferdig-count-{count}", "#qe-job-indicator")
            prev_count = count

        if count == 0:
            print("  ✓ Alle bygg ferdige – indikator borte")
            break
    else:
        print("  ⚠ Timeout (3 min) – bygg ikke ferdig")
        await screenshot(page, "08-timeout")


async def step_09_final_state(page: Page):
    print("\n[9/9] Verifiserer slutt-tilstand…")
    state = await get_pending_state(page)
    ind_visible = await page.evaluate(
        "document.getElementById('qe-job-indicator')?.style.display === 'flex'"
    )

    if not state and not ind_visible:
        print("  ✅ PASS: Ingen ventende state og indikator er skjult")
    elif state:
        print(f"  ⚠ State fortsatt i localStorage: {state}")
    elif ind_visible:
        print(f"  ⚠ Indikator fortsatt synlig: «{await get_indicator_text(page)}»")

    await screenshot(page, "09-slutt-tilstand")

    # Oppsummering
    print(f"\n{'='*50}")
    print(f"Screenshots lagret i: {SCREENSHOTS}")
    print(f"{'='*50}")
    imgs = sorted(SCREENSHOTS.glob("*.png"))
    for img in imgs:
        print(f"  {img.name}")


# ---------------------------------------------------------------------------
# Hovedfunksjon
# ---------------------------------------------------------------------------

async def main():
    if not GH_TOKEN:
        print("❌  Sett GITHUB_TOKEN før kjøring:")
        print("    GITHUB_TOKEN=ghp_... python test_pending_indicator.py")
        sys.exit(1)

    print(f"🚀 SAMT-BU Docs – pending-indikator E2E-test")
    print(f"   URL:   {BASE_URL + TEST_PAGE}")
    print(f"   Bruker: {GH_USER or '(GITHUB_USER ikke satt)'}")
    print(f"   Headless: {HEADLESS}")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO,
            args=["--start-maximized"]
        )
        context: BrowserContext = await browser.new_context(
            no_viewport=True,  # Respekter --start-maximized
            record_video_dir=str(SCREENSHOTS / "video") if not HEADLESS else None
        )
        page = await context.new_page()

        try:
            await step_01_load_site(page)
            await step_02_inject_and_reload(page)
            await step_03_open_edit_menu(page)
            await step_04_open_edit_dialog(page)
            await step_05_make_change(page)
            await step_06_save_and_observe_indicator(page)
            await step_07_navigate_away(page)
            await step_08_wait_for_build_and_countdown(page)
            await step_09_final_state(page)
        except Exception as e:
            await screenshot(page, "XX-feil-ved-krasj")
            print(f"\n❌ Test krasjet: {e}")
            raise
        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
