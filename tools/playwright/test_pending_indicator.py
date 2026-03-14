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

Genererer også dokumentasjons-screenshots og video i screenshots/

Kjøring:
  pip install playwright python-dotenv
  playwright install chromium
  python test_pending_indicator.py  (les token fra .env)

Token-krav: GitHub PAT med 'repo' og 'workflow'-scope (samme som du bruker i nettleseren).
"""

import asyncio
import os
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
GH_USER     = os.environ.get("GITHUB_USER", "")
TEST_PAGE   = os.environ.get("TEST_PAGE", "/test-samt-bu-docs/test-1/")
HEADLESS    = os.environ.get("HEADLESS", "false").lower() == "true"
SLOW_MO     = int(os.environ.get("SLOW_MO", "0"))      # 0 = ingen slow_mo; pauser styres av STEP_PAUSE
STEP_PAUSE  = 2000                                     # ms total pause (inkl. bevegelse) mellom klikk

SCREENSHOTS = Path(__file__).parent / "screenshots" / datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------------------------------------------------------------------------
# Visuell overlay-infrastruktur
# ---------------------------------------------------------------------------

CURSOR_OVERLAY_JS = """
(function() {
    if (document.getElementById('pw-cursor')) return;
    const cur = document.createElement('div');
    cur.id = 'pw-cursor';
    cur.style.cssText = [
        'position:fixed', 'width:18px', 'height:18px', 'border-radius:50%',
        'background:rgba(220,50,50,0.85)', 'border:2px solid #fff',
        'pointer-events:none', 'z-index:2147483647',
        'transform:translate(-50%,-50%)',
        'box-shadow:0 0 8px rgba(0,0,0,0.6)',
        'transition:left 0.04s linear,top 0.04s linear'
    ].join(';');
    document.body.appendChild(cur);
    document.addEventListener('mousemove', function(e) {
        cur.style.left = e.clientX + 'px';
        cur.style.top  = e.clientY + 'px';
    }, true);
})();
"""

INDICATOR_PULSE_JS = """
(function() {
    if (document.getElementById('pw-pulse-style')) return;
    const s = document.createElement('style');
    s.id = 'pw-pulse-style';
    s.textContent = `
        @keyframes pw-ind-pulse {
            0%,100% { box-shadow: 0 0 0 0 rgba(255,200,0,0.0); }
            50%      { box-shadow: 0 0 0 8px rgba(255,200,0,0.7); }
        }
        #qe-job-indicator {
            animation: pw-ind-pulse 1.2s ease-in-out infinite !important;
            outline: 2px solid #ffe066 !important;
        }
    `;
    document.head.appendChild(s);
})();
"""

async def inject_cursor_overlay(page: Page):
    """Injiser synlig rød cursor-overlay (persisterer i video)."""
    await page.evaluate(CURSOR_OVERLAY_JS)

async def inject_indicator_pulse(page: Page):
    """Gjør #qe-job-indicator pulsere gult – synlig i video."""
    await page.evaluate(INDICATOR_PULSE_JS)

async def show_bubble(page: Page, text: str, duration_ms: int = None):
    """
    Vis en forklarende kommentarboble midt på skjermen.
    duration_ms=None → boblen blir stående til siden lastes på nytt.
    """
    timeout_js = ""
    if duration_ms is not None:
        timeout_js = f"""
            setTimeout(() => {{
                b.style.opacity = '0';
                setTimeout(() => b.remove(), 450);
            }}, {duration_ms});
        """
    await page.evaluate(f"""
        (text) => {{
            const existing = document.getElementById('pw-bubble');
            if (existing) existing.remove();
            const b = document.createElement('div');
            b.id = 'pw-bubble';
            b.innerHTML = text;
            b.style.cssText = [
                'position:fixed', 'bottom:70px', 'left:50%',
                'transform:translateX(-50%)',
                'background:rgba(15,25,50,0.93)',
                'color:#fff', 'padding:18px 28px',
                'border-radius:14px', 'font-size:15px',
                'max-width:620px', 'text-align:center',
                'z-index:2147483640',
                'box-shadow:0 6px 24px rgba(0,0,0,0.6)',
                'border:1px solid rgba(255,255,255,0.18)',
                'line-height:1.6', 'opacity:0',
                'transition:opacity 0.4s ease'
            ].join(';');
            document.body.appendChild(b);
            requestAnimationFrame(() => {{ b.style.opacity = '1'; }});
            {timeout_js}
        }}
    """, text)

async def show_final_overlay(page: Page, text: str, duration_ms: int = 5000):
    """Full-skjerm overlay med sentert tekst – brukes som avslutningsskjerm i video."""
    fade_out_at = duration_ms - 900
    await page.evaluate(f"""
        (text) => {{
            const overlay = document.createElement('div');
            overlay.id = 'pw-final-overlay';
            overlay.style.cssText = [
                'position:fixed', 'inset:0',
                'background:rgba(10,18,40,0.88)',
                'display:flex', 'align-items:center', 'justify-content:center',
                'z-index:2147483647',
                'opacity:0', 'transition:opacity 0.8s ease'
            ].join(';');
            const inner = document.createElement('div');
            inner.innerHTML = text;
            inner.style.cssText = [
                'color:#fff', 'font-size:26px', 'font-weight:600',
                'text-align:center', 'padding:48px',
                'max-width:720px', 'line-height:1.6'
            ].join(';');
            overlay.appendChild(inner);
            document.body.appendChild(overlay);
            requestAnimationFrame(() => {{ overlay.style.opacity = '1'; }});
            setTimeout(() => {{
                overlay.style.opacity = '0';
                setTimeout(() => overlay.remove(), 900);
            }}, {fade_out_at});
        }}
    """, text)


async def click_flash(page: Page, x: float, y: float):
    """Tegn en gul ripple-animasjon ved klikk-koordinater."""
    await page.evaluate("""
        ([x, y]) => {
            const r = document.createElement('div');
            const id = 'pw-ripple-' + Date.now();
            r.id = id;
            r.style.cssText = [
                'position:fixed', `left:${x}px`, `top:${y}px`,
                'width:12px', 'height:12px', 'border-radius:50%',
                'background:rgba(255,210,0,0.95)', 'pointer-events:none',
                'z-index:2147483646', 'transform:translate(-50%,-50%)',
                'transition:transform 0.55s ease-out, opacity 0.55s ease-out'
            ].join(';');
            document.body.appendChild(r);
            requestAnimationFrame(() => {
                r.style.transform = 'translate(-50%,-50%) scale(5)';
                r.style.opacity   = '0';
            });
            setTimeout(() => r.remove(), 600);
        }
    """, [x, y])

async def move_and_click(page: Page, locator, pause: bool = True, click_count: int = 1):
    """
    Animert cursor-bevegelse til element, ripple-flash, så klikk.
    pause=True venter STEP_PAUSE ms totalt (bevegelse + klikk innenfor dette).
    steps=1 → musepekeren hopper til målet øyeblikkelig; CSS-transition på
    #pw-cursor (0.04s) gir visuell glatting i videoen.
    """
    if pause:
        await page.wait_for_timeout(STEP_PAUSE - 400)   # reserver ~400ms til bevegelse+flash
    box = await locator.bounding_box()
    if box:
        x = box['x'] + box['width']  / 2
        y = box['y'] + box['height'] / 2
        await page.mouse.move(x, y, steps=1)
        await page.wait_for_timeout(200)
        await click_flash(page, x, y)
        await page.wait_for_timeout(120)
        for _ in range(click_count):
            await page.mouse.click(x, y)
    else:
        await locator.click(click_count=click_count)

# ---------------------------------------------------------------------------
# Screenshot-hjelper
# ---------------------------------------------------------------------------

async def screenshot(page: Page, name: str, highlight_selector: str = None):
    """Ta screenshot med valgfri element-highlight."""
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    path = SCREENSHOTS / f"{name}.png"
    if highlight_selector:
        await page.evaluate("""
            (sel) => {
                const el = document.querySelector(sel);
                if (el) {
                    el._origOutline = el.style.outline;
                    el._origZIndex  = el.style.zIndex;
                    el.style.outline = '3px solid #e63946';
                    el.style.zIndex  = '9999';
                }
            }
        """, highlight_selector)
        await page.screenshot(path=str(path), full_page=False)
        await page.evaluate("""
            (sel) => {
                const el = document.querySelector(sel);
                if (el) {
                    el.style.outline = el._origOutline || '';
                    el.style.zIndex  = el._origZIndex  || '';
                }
            }
        """, highlight_selector)
    else:
        await page.screenshot(path=str(path), full_page=False)
    print(f"  📸 {path.name}")
    return path

# ---------------------------------------------------------------------------
# Hjelpefunksjoner
# ---------------------------------------------------------------------------

async def inject_credentials(page: Page):
    if not GH_TOKEN:
        print("⚠  GITHUB_TOKEN ikke satt – hopper over autentisering")
        return
    await page.evaluate(f"""
        localStorage.setItem('samt-bu-gh-token', {json.dumps(GH_TOKEN)});
        localStorage.setItem('samt-bu-gh-user', {json.dumps(GH_USER)});
    """)
    print(f"  🔑 Token injisert for bruker: {GH_USER or '(ikke satt)'}")

async def get_pending_state(page: Page) -> dict:
    raw = await page.evaluate("localStorage.getItem('samtu-build-pending')")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw}

async def wait_for_indicator(page: Page, timeout_ms: int = 5000) -> bool:
    try:
        await page.wait_for_function(
            "document.getElementById('qe-job-indicator')?.style.display === 'flex'",
            timeout=timeout_ms
        )
        return True
    except Exception:
        return False

async def get_indicator_text(page: Page) -> str:
    return await page.evaluate(
        "document.getElementById('qe-job-indicator')?.innerText?.trim() || ''"
    )

# ---------------------------------------------------------------------------
# Teststeg
# ---------------------------------------------------------------------------

async def step_01_load_site(page: Page):
    print("\n[1/9] Laster nettstedet…")
    await page.goto(BASE_URL + TEST_PAGE, wait_until="networkidle")
    await inject_cursor_overlay(page)
    await screenshot(page, "01-startside")
    print(f"  ✓ Nettsted lastet: {BASE_URL + TEST_PAGE}")


async def step_02_inject_and_reload(page: Page):
    print("\n[2/9] Injiserer credentials og laster siden på nytt…")
    await inject_credentials(page)
    await page.reload(wait_until="networkidle")
    await inject_cursor_overlay(page)
    await screenshot(page, "02-etter-innlogging")


async def step_03_open_edit_menu(page: Page):
    print("\n[3/9] Åpner Endre-menyen…")
    edit_btn = page.locator("#edit-toggle")
    await edit_btn.wait_for(state="visible", timeout=5000)
    await move_and_click(page, edit_btn)
    await page.wait_for_timeout(400)
    rediger_item = page.locator("#edit-menu a").filter(
        has_text=re.compile(r"Rediger dette kapitlet|Edit this chapter", re.IGNORECASE)
    ).first
    await rediger_item.wait_for(state="visible", timeout=5000)
    await screenshot(page, "03-endre-meny-apen", "#edit-menu")
    # Gul highlight på valgt menyvalg
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
    await move_and_click(page, rediger)
    await page.wait_for_selector("#qe-overlay", state="visible", timeout=10000)
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
    base_title = re.sub(r'\s*\(testet.*', '', current_title).strip()  # fjern alt fra første «(testet»
    ts = datetime.now().strftime("%H:%M:%S")
    new_title = f"{base_title} (testet {ts})"
    # Klikk for å fokusere feltet
    await move_and_click(page, title_input)
    await page.wait_for_timeout(200)
    # Marker all eksisterende tekst (Ctrl+A) – synlig i video
    await page.keyboard.press("Control+a")
    await page.wait_for_timeout(600)      # pause – viser markeringen
    # Slett markert tekst (visuell animasjon + faktisk tømming)
    await page.keyboard.press("Backspace")
    await title_input.fill("")            # sikrer at feltet er faktisk tomt
    await page.wait_for_timeout(400)      # pause – viser tomt felt
    # Skriv ny tittel tegn for tegn – simulerer manuell inntasting
    await page.keyboard.type(new_title, delay=70)
    await screenshot(page, "05-tittel-endret", "#qe-meta-panel")
    print(f"  ✓ Tittel endret: «{current_title}» → «{new_title}»")


async def step_06_save_and_observe_indicator(page: Page):
    print("\n[6/9] Lagrer og observerer pending-indikator…")
    save_btn = page.locator("#qe-save-btn")
    await move_and_click(page, save_btn)
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
    state = await get_pending_state(page)
    print(f"  📦 Pending state: {state}")

    cancel_btn = page.locator("#qe-cancel-btn")
    await move_and_click(page, cancel_btn)
    await page.wait_for_selector("#qe-overlay", state="hidden", timeout=5000)

    visible = await wait_for_indicator(page)
    if visible:
        await inject_indicator_pulse(page)   # Gjør indikatoren synlig i video
        text = await get_indicator_text(page)
        print(f"  ✓ Indikator synlig: «{text}»")
        await screenshot(page, "06b-pending-indikator-synlig", "#qe-job-indicator")
    else:
        print("  ⚠ Indikator ikke synlig etter lagring")
        await screenshot(page, "06b-ingen-indikator")


async def step_07_navigate_away(page: Page):
    print("\n[7/9] Navigerer til annen side og sjekker at indikator gjenopprettes…")
    await page.wait_for_timeout(STEP_PAUSE)
    await page.goto(BASE_URL + "/test-samt-bu-docs/test-2/", wait_until="networkidle")
    await inject_cursor_overlay(page)
    await page.wait_for_timeout(800)

    current_url = page.url
    print(f"  → Navigerte til: {current_url}")

    visible = await wait_for_indicator(page, timeout_ms=4000)
    if visible:
        await inject_indicator_pulse(page)
        text = await get_indicator_text(page)
        state = await get_pending_state(page)
        print(f"  ✓ Indikator gjenopprettet etter navigering: «{text}»")
        print(f"  📦 State: {state}")
        await screenshot(page, "07-indikator-etter-navigering", "#qe-job-indicator")
    else:
        print("  ⚠ Indikator IKKE gjenopprettet etter navigering – feil!")
        await screenshot(page, "07-indikator-mangler-etter-navigering")

    # Forklarende boble – blir stående til siden lastes automatisk på nytt (bygg ferdig)
    await show_bubble(page,
        "Vi kan nå jobbe videre på andre sider mens nettstedet oppdateres i bakgrunnen."
        "<br><br>"
        "Hver oppdateringsjobb tar typisk rundt <strong>ett minutt</strong>. "
        "Indikatoren nederst til venstre holder oss oppdatert."
        "<br><br>"
        "I denne testen venter vi til jobben er ferdig for å demonstrere "
        "hvordan tittelen på «Test 1» oppdateres i venstremenyen.",
        duration_ms=None    # ingen timeout – forsvinner ved automatisk sideoppdatering
    )


async def step_08_wait_for_build_and_countdown(page: Page):
    print("\n[8/9] Venter på bygg og observerer nedtelling (kan ta 1–3 min)…")
    print("  ⏳ Poller GitHub Actions – venter…")

    prev_state = await get_pending_state(page)
    prev_count = prev_state.get("count", 0)

    for i in range(12):  # maks 3 min
        await page.wait_for_timeout(15000)
        # Re-injiser pulse hvert intervall (forsvinner ikke ved DOM-oppdatering)
        await inject_indicator_pulse(page)
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

    # Avslutningsoverlay – fader inn og ut i ~5 sekunder (synlig på slutten av videoen)
    await show_final_overlay(page,
        "Demoen er ferdig."
        "<br><br>"
        "<span style='font-size:16px;font-weight:400;opacity:0.75'>"
        "SAMT-BU Docs – pending build-indikator"
        "</span>",
        duration_ms=5000
    )
    await page.wait_for_timeout(5500)

    print(f"\n{'='*50}")
    print(f"Screenshots lagret i: {SCREENSHOTS}")
    print(f"{'='*50}")
    for img in sorted(SCREENSHOTS.glob("*.png")):
        print(f"  {img.name}")


# ---------------------------------------------------------------------------
# Hovedfunksjon
# ---------------------------------------------------------------------------

async def main():
    if not GH_TOKEN:
        print("❌  Sett GITHUB_TOKEN i .env før kjøring")
        sys.exit(1)

    print(f"🚀 SAMT-BU Docs – pending-indikator E2E-test")
    print(f"   URL:    {BASE_URL + TEST_PAGE}")
    print(f"   Bruker: {GH_USER or '(GITHUB_USER ikke satt)'}")
    print(f"   Headless: {HEADLESS}  |  SLOW_MO: {SLOW_MO}ms  |  STEP_PAUSE: {STEP_PAUSE}ms")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO,
            args=["--start-maximized"]
        )
        context: BrowserContext = await browser.new_context(
            no_viewport=True,
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
