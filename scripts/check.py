#!/usr/bin/env python3
"""Site checks: every top-level *.html x {V1, V2} x {1440x900, 390x844}. Ends with ALL PASS or FAIL: ... (exit 1).
Run with ~/.venvs/automation/bin/python (needs Playwright + Chromium)."""
import functools, http.server, re, sys, threading
from pathlib import Path
from urllib.parse import urldefrag, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from build_v2 import render  # noqa: E402

PLANNED = {"index.html", "about.html", "services.html", "brands.html", "shop.html", "product.html", "contact.html"}
VIEWPORTS = [(1440, 900), (390, 844)]
SHOTS = ROOT / "research" / "screens"


def serve():
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(H, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def check_links(hrefs, page_file):
    """Return (errors, pending). Links to planned-but-unbuilt pages are pending, not errors."""
    errs, pending = [], set()
    for h in hrefs:
        if re.match(r"^(https?:|mailto:|tel:|data:|javascript:)", h):
            continue
        path, frag = urldefrag(h)
        target = page_file if not path else (page_file.parent / urlparse(path).path).resolve()
        if not target.exists():
            if target.name in PLANNED and target.parent in (ROOT, ROOT / "v2"):
                pending.add(target.name)
            else:
                errs.append(f"missing file {h}")
            continue
        if frag and target.suffix == ".html" and not re.search(rf'\bid="{re.escape(frag)}"', target.read_text()):
            errs.append(f"missing anchor {h}")
    return errs, pending


def main():
    pages = sorted(p.name for p in ROOT.glob("*.html"))
    fails = []
    v2 = ROOT / "v2"
    if sorted(p.name for p in v2.glob("*.html")) != pages:
        fails.append("v2/ page set differs from root (run scripts/build_v2.py)")
    for n in pages:
        f = v2 / n
        if not f.exists() or f.read_text() != render((ROOT / n).read_text()):
            fails.append(f"v2/{n} is stale (run scripts/build_v2.py)")
    SHOTS.mkdir(parents=True, exist_ok=True)
    srv, port = serve()
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for variant, prefix in (("v1", ""), ("v2", "v2/")):
            for n in pages:
                for w, h in VIEWPORTS:
                    ctx = browser.new_context(viewport={"width": w, "height": h})
                    pg = ctx.new_page()
                    errors = []
                    # web-font fetches may fail offline; that is not a site bug
                    pg.on("console", lambda m: m.type == "error" and "fonts.g" not in (m.location.get("url") or "") and errors.append(m.text))
                    pg.on("pageerror", lambda e: errors.append(str(e)))
                    pg.goto(f"http://127.0.0.1:{port}/{prefix}{n}", wait_until="load")
                    pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
                    pg.wait_for_function("[...document.images].every(i=>i.complete)", timeout=15000)
                    y = 0
                    while y < pg.evaluate("document.documentElement.scrollHeight"):  # scroll through so .reveal fires
                        y += 500
                        pg.evaluate(f"scrollTo(0,{y})")
                        pg.wait_for_timeout(60)
                    pg.evaluate("scrollTo(0,0)")
                    pg.wait_for_timeout(900)
                    problems = list(errors)
                    over = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
                    if over > 0:
                        problems.append(f"horizontal overflow {over}px")
                    broken = pg.evaluate("[...document.images].filter(i=>!i.naturalWidth).map(i=>i.getAttribute('src'))")
                    if broken:
                        problems.append(f"broken images {broken}")
                    hrefs = pg.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))")
                    lerr, pending = check_links(hrefs, ROOT / prefix / n)
                    problems += lerr
                    ph = pg.evaluate("document.querySelectorAll('.ph').length")
                    hov = "-"
                    if w == 1440 and pg.query_selector("main .lamp"):
                        before = pg.evaluate("getComputedStyle(document.querySelector('main .lamp img')).filter")
                        pg.hover("main .lamp")
                        pg.wait_for_timeout(800)
                        after = pg.evaluate("getComputedStyle(document.querySelector('main .lamp img')).filter")
                        hov = "ok" if before != after else "SAME"
                        if before == after:
                            problems.append(f"hover filter unchanged ({before})")
                    pg.mouse.move(0, 0)
                    pg.screenshot(path=str(SHOTS / f"{variant}-{n[:-5]}-{w}.png"), full_page=True)
                    rows.append((variant, n, w, ph, hov, len(pending), "ok" if not problems else "; ".join(problems)))
                    fails += [f"{variant}/{n}@{w}: {p}" for p in problems]
                    ctx.close()
        browser.close()
    srv.shutdown()
    print(f"{'variant':7} {'page':14} {'w':5} {'.ph':4} {'hover':6} {'pend':4} result")
    for r in rows:
        print(f"{r[0]:7} {r[1]:14} {r[2]:<5} {r[3]:<4} {r[4]:6} {r[5]:<4} {r[6]}")
    print("(pend = distinct linked pages not built yet; planned in the brief site map)")
    print("ALL PASS" if not fails else "FAIL: " + " | ".join(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
