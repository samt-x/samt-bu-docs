# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
Playwright E2E-test: To ventende byggejobber (samme bruker)
============================================================

Tester at pending-indikatoren:
  1. Viser count=1 etter første lagring
  2. Viser count=2 etter andre lagring (på en annen side)
  3. Gjenopprettes korrekt etter sidenavigering
  4. Decrementerer én gang per ferdig bygg (2 → 1 → 0)
  5. Forsvinner når count = 0

Kjøring:
  pip install playwright python-dotenv
  playwright install chromium
  python test_two_pending_jobs.py

Token-krav: GitHub PAT med 'repo' og 'workflow'-scope.
"""

import asyncio
import os
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, BrowserContext

# ---------------------------------------------------------------------------
# Video-konfigurasjon
# ---------------------------------------------------------------------------

VIDEO_W = 1920
VIDEO_H = 1080

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
TEST_PAGE   = os.environ.get("TEST_PAGE",   "/test-samt-bu-docs/test-1/")
TEST_PAGE_2 = os.environ.get("TEST_PAGE_2", "/test-samt-bu-docs/test-2/")
HEADLESS    = os.environ.get("HEADLESS", "false").lower() == "true"
SLOW_MO     = int(os.environ.get("SLOW_MO", "0"))
STEP_PAUSE  = 300   # ms pause før cursor flyttes

SCREENSHOTS = Path(__file__).parent / "screenshots" / datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------------------------------------------------------------------------
# Visuell overlay-infrastruktur (identisk med test 1)
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
    await page.evaluate(CURSOR_OVERLAY_JS)

async def inject_indicator_pulse(page: Page):
    await page.evaluate(INDICATOR_PULSE_JS)

async def show_bubble(page: Page, text: str, duration_ms: int = None):
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
                'position:fixed', 'bottom:160px', 'left:50%',
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
    if pause:
        await page.wait_for_timeout(STEP_PAUSE)
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

async def do_edit_and_save(page: Page, step_prefix: str, page_label: str) -> str:
    """
    Åpner Endre-menyen, åpner redigeringsdialogen, endrer tittelen og lagrer.
    Returnerer den nye tittelen.
    Brukes for begge Test 1 og Test 2.
    """
    print(f"  → Åpner Endre-meny på {page_label}…")
    edit_btn = page.locator("#edit-toggle")
    await edit_btn.wait_for(state="visible", timeout=5000)
    await move_and_click(page, edit_btn)
    await page.wait_for_timeout(400)

    rediger = page.locator("#edit-menu a").filter(
        has_text=re.compile(r"Rediger dette kapitlet|Edit this chapter", re.IGNORECASE)
    ).first
    await rediger.wait_for(state="visible", timeout=5000)
    await screenshot(page, f"{step_prefix}-endre-meny-apen", "#edit-menu")

    print(f"  → Åpner redigeringsdialog på {page_label}…")
    await move_and_click(page, rediger)
    await page.wait_for_selector("#qe-overlay", state="visible", timeout=10000)
    await page.wait_for_function(
        "document.getElementById('qe-field-title')?.value?.length > 0",
        timeout=15000
    )
    await screenshot(page, f"{step_prefix}-dialog-apen", "#qe-meta-panel")

    print(f"  → Endrer tittel på {page_label}…")
    title_input = page.locator("#qe-field-title")
    await title_input.wait_for(state="visible", timeout=10000)
    current_title = await title_input.input_value()
    base_title = re.sub(r'\s*\(testet.*', '', current_title).strip()
    ts = datetime.now().strftime("%H:%M:%S")
    new_title = f"{base_title} (testet {ts})"
    await move_and_click(page, title_input)
    await page.wait_for_timeout(150)
    await page.keyboard.press("Control+a")
    await page.wait_for_timeout(600)
    await page.keyboard.type(new_title, delay=70)
    await screenshot(page, f"{step_prefix}-tittel-endret", "#qe-meta-panel")

    print(f"  → Lagrer {page_label}…")
    save_btn = page.locator("#qe-save-btn")
    await move_and_click(page, save_btn)
    try:
        await page.wait_for_function(
            "document.getElementById('qe-status-text')?.textContent?.includes('Lagret') "
            "|| document.getElementById('qe-status-text')?.textContent?.includes('Saved')",
            timeout=30000
        )
        print(f"  ✓ Commit sendt for {page_label}")
    except Exception:
        print(f"  ⚠ Timeout – commit kanskje ikke sendt for {page_label}")

    await page.wait_for_timeout(500)
    await screenshot(page, f"{step_prefix}-etter-lagring", "#qe-overlay")
    state = await get_pending_state(page)
    print(f"  📦 Pending state etter lagring: {state}")

    cancel_btn = page.locator("#qe-cancel-btn")
    await move_and_click(page, cancel_btn)
    await page.wait_for_selector("#qe-overlay", state="hidden", timeout=5000)

    return new_title

# ---------------------------------------------------------------------------
# Teststeg
# ---------------------------------------------------------------------------

async def step_01_load_and_auth(page: Page):
    print("\n[1/9] Laster nettstedet og injiserer credentials…")
    await page.goto(BASE_URL + TEST_PAGE, wait_until="networkidle")
    await inject_cursor_overlay(page)
    await inject_credentials(page)
    await page.reload(wait_until="networkidle")
    await inject_cursor_overlay(page)
    await screenshot(page, "01-startside-etter-innlogging")
    print(f"  ✓ Nettsted lastet: {BASE_URL + TEST_PAGE}")


async def step_02_edit_test1(page: Page):
    print("\n[2/9] Redigerer og lagrer Test 1 (første jobb i kø)…")
    await do_edit_and_save(page, "02", "Test 1")

    # Vent på og vis indikatoren (count=1)
    visible = await wait_for_indicator(page)
    if visible:
        await inject_indicator_pulse(page)
        text = await get_indicator_text(page)
        state = await get_pending_state(page)
        count = state.get("count", "?")
        print(f"  ✓ Indikator synlig med count={count}: «{text}»")
        await screenshot(page, "02-indikator-count-1", "#qe-job-indicator")
    else:
        print("  ⚠ Indikator ikke synlig etter første lagring")
        await screenshot(page, "02-ingen-indikator")


async def step_03_navigate_to_test2(page: Page):
    print("\n[3/9] Navigerer til Test 2 – sjekker at indikator (count=1) gjenopprettes…")
    await page.goto(BASE_URL + TEST_PAGE_2, wait_until="networkidle")
    await inject_cursor_overlay(page)
    await page.wait_for_timeout(600)
    print(f"  → Navigerte til: {page.url}")

    visible = await wait_for_indicator(page, timeout_ms=4000)
    if visible:
        await inject_indicator_pulse(page)
        text = await get_indicator_text(page)
        state = await get_pending_state(page)
        count = state.get("count", "?")
        print(f"  ✓ Indikator gjenopprettet på Test 2 med count={count}: «{text}»")
        await screenshot(page, "03-test2-indikator-count-1", "#qe-job-indicator")
    else:
        print("  ⚠ Indikator IKKE gjenopprettet etter navigering – feil!")
        await screenshot(page, "03-indikator-mangler")


async def step_04_edit_test2(page: Page):
    print("\n[4/9] Redigerer og lagrer Test 2 (andre jobb i kø)…")
    await do_edit_and_save(page, "04", "Test 2")

    # Nå skal count=2
    visible = await wait_for_indicator(page)
    if visible:
        await inject_indicator_pulse(page)
        text = await get_indicator_text(page)
        state = await get_pending_state(page)
        count = state.get("count", "?")
        print(f"  ✓ Indikator synlig med count={count}: «{text}»")
        if count == 2:
            print("  ✅ count=2 bekreftet – to jobber i kø!")
        else:
            print(f"  ⚠ Forventet count=2, fikk count={count}")
        await screenshot(page, "04-indikator-count-2", "#qe-job-indicator")
    else:
        print("  ⚠ Indikator ikke synlig etter andre lagring")
        await screenshot(page, "04-ingen-indikator")


async def step_05_navigate_to_test1(page: Page):
    print("\n[5/9] Navigerer tilbake til Test 1 – sjekker at indikator (count=2) gjenopprettes…")
    await page.goto(BASE_URL + TEST_PAGE, wait_until="networkidle")
    await inject_cursor_overlay(page)
    await page.wait_for_timeout(600)
    print(f"  → Navigerte til: {page.url}")

    visible = await wait_for_indicator(page, timeout_ms=4000)
    if visible:
        await inject_indicator_pulse(page)
        text = await get_indicator_text(page)
        state = await get_pending_state(page)
        count = state.get("count", "?")
        print(f"  ✓ Indikator gjenopprettet på Test 1 med count={count}: «{text}»")
        await screenshot(page, "05-test1-indikator-count-2", "#qe-job-indicator")
    else:
        print("  ⚠ Indikator IKKE gjenopprettet etter navigering – feil!")
        await screenshot(page, "05-indikator-mangler")


async def step_06_wait_for_first_build(page: Page):
    print("\n[6/9] Venter på første bygg (count: 2 → 1)…")
    print("  ⏳ Poller GitHub Actions – venter…")

    prev_count = 2
    for i in range(12):  # maks 3 min
        await page.wait_for_timeout(15000)
        try:
            await inject_indicator_pulse(page)
            state   = await get_pending_state(page)
            count   = state.get("count", 0)
            ind_txt = await get_indicator_text(page)
        except Exception:
            print(f"  ⏱ {(i+1)*15}s – side lastes på nytt…")
            continue

        print(f"  ⏱ {(i+1)*15}s – count={count}, indikator: «{ind_txt}»")

        if count < prev_count:
            print(f"  ✓ Første bygg ferdig – count decrementert: {prev_count} → {count}")
            await screenshot(page, f"06-etter-forste-bygg-count-{count}", "#qe-job-indicator")
            prev_count = count
            if count <= 1:
                break

    if prev_count > 1:
        print("  ⚠ Timeout (3 min) – første bygg ikke ferdig")
        await screenshot(page, "06-timeout-forste-bygg")


async def step_07_wait_for_second_build(page: Page):
    print("\n[7/9] Venter på andre bygg (count: 1 → 0)…")
    print("  ⏳ Poller GitHub Actions – venter…")

    state = await get_pending_state(page)
    prev_count = state.get("count", 1)

    if prev_count == 0:
        print("  ℹ Begge bygg allerede ferdige – hopper over polling")
        return

    for i in range(12):  # maks 3 min
        await page.wait_for_timeout(15000)
        try:
            await inject_indicator_pulse(page)
            state   = await get_pending_state(page)
            count   = state.get("count", 0)
            ind_txt = await get_indicator_text(page)
        except Exception:
            print(f"  ⏱ {(i+1)*15}s – side lastes på nytt…")
            continue

        print(f"  ⏱ {(i+1)*15}s – count={count}, indikator: «{ind_txt}»")

        if count < prev_count or count == 0:
            print(f"  ✓ Andre bygg ferdig – count decrementert: {prev_count} → {count}")
            await screenshot(page, f"07-etter-andre-bygg-count-{count}", "#qe-job-indicator")
            prev_count = count

        if count == 0:
            print("  ✅ Begge bygg ferdige – indikator borte")
            break
    else:
        print("  ⚠ Timeout (3 min) – andre bygg ikke ferdig")
        await screenshot(page, "07-timeout-andre-bygg")


async def step_08_verify_sidebar_titles(page: Page):
    print("\n[8/9] Verifiserer at oppdaterte titler vises i venstremenyen…")
    await page.wait_for_timeout(1000)

    test1_link = page.locator("#sidebar a").filter(
        has_text=re.compile(r"Test\s+1", re.IGNORECASE)
    ).first
    test2_link = page.locator("#sidebar a").filter(
        has_text=re.compile(r"Test\s+2", re.IGNORECASE)
    ).first

    t1_text = await test1_link.inner_text() if await test1_link.count() > 0 else "(ikke funnet)"
    t2_text = await test2_link.inner_text() if await test2_link.count() > 0 else "(ikke funnet)"
    print(f"  Test 1 i sidebar: «{t1_text.strip()}»")
    print(f"  Test 2 i sidebar: «{t2_text.strip()}»")
    await screenshot(page, "08-sidebar-titler-oppdatert", "#sidebar")


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

    await show_final_overlay(page,
        "Demoen er ferdig."
        "<br><br>"
        "<span style='font-size:16px;font-weight:400;opacity:0.75'>"
        "SAMT-BU Docs – to ventende byggejobber (én bruker)"
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

    print(f"🚀 SAMT-BU Docs – to ventende byggejobber (E2E-test)")
    print(f"   Side 1: {BASE_URL + TEST_PAGE}")
    print(f"   Side 2: {BASE_URL + TEST_PAGE_2}")
    print(f"   Bruker: {GH_USER or '(GITHUB_USER ikke satt)'}")
    print(f"   Headless: {HEADLESS}  |  SLOW_MO: {SLOW_MO}ms  |  STEP_PAUSE: {STEP_PAUSE}ms")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO,
            args=[]
        )
        context: BrowserContext = await browser.new_context(
            viewport={"width": VIDEO_W, "height": VIDEO_H},
            record_video_size={"width": VIDEO_W, "height": VIDEO_H},
            record_video_dir=str(SCREENSHOTS / "video") if not HEADLESS else None
        )
        page = await context.new_page()

        try:
            await step_01_load_and_auth(page)
            await step_02_edit_test1(page)
            await step_03_navigate_to_test2(page)
            await step_04_edit_test2(page)
            await step_05_navigate_to_test1(page)
            await step_06_wait_for_first_build(page)
            await step_07_wait_for_second_build(page)
            await step_08_verify_sidebar_titles(page)
            await step_09_final_state(page)
        except Exception as e:
            await screenshot(page, "XX-feil-ved-krasj")
            print(f"\n❌ Test krasjet: {e}")
            raise
        finally:
            await context.close()
            await browser.close()

    # Flytt .webm til demo.webm i screenshot-mappen
    if not HEADLESS:
        video_dir = SCREENSHOTS / "video"
        webms = list(video_dir.glob("*.webm"))
        if webms:
            dest = SCREENSHOTS / "demo.webm"
            shutil.move(str(webms[0]), dest)
            video_dir.rmdir()
            print(f"\n🎬 Video: {dest}")

    # Kopier viewer.html inn i screenshot-mappen
    viewer_src = Path(__file__).parent / "viewer.html"
    if viewer_src.exists():
        shutil.copy(viewer_src, SCREENSHOTS / "viewer.html")
        print(f"  📄 viewer.html kopiert – åpne {SCREENSHOTS / 'viewer.html'} i nettleser")


if __name__ == "__main__":
    asyncio.run(main())
