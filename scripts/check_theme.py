#!/usr/bin/env python3
"""Shopify theme checks via `shopify theme dev` proxy (store password from ~/automation/lightform/env).
Usage: ~/.venvs/automation/bin/python scripts/check_theme.py [--theme ID]. Ends ALL PASS (0) / FAIL: ... (1) / SKIP (2)."""
import os, re, signal, subprocess, sys, time, urllib.request
from collections import deque
from pathlib import Path
from urllib.parse import urldefrag

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "research" / "screens" / "theme"
ENV = Path.home() / "automation" / "lightform" / "env"
STORE, BASE = "26gcsf-0y.myshopify.com", "http://127.0.0.1:9292"
VIEWPORTS = [(1440, 900), (390, 844)]
ROUTES = ["/", "/pages/about", "/pages/services", "/pages/brands", "/pages/contact", "/collections",
          "/collections/all", "/collections/shop-maju-design",
          "/collections/objects-and-living", "/cart", "/search?q=light", "/search?q=lamp", "/this-page-does-not-exist"]


def main():
    if not ENV.exists():
        print("SKIP: ~/automation/lightform/env not found (store password)"); sys.exit(2)
    env = dict(os.environ)
    for line in ENV.read_text().splitlines():
        k, _, v = line.partition("=")
        if k.strip() == "SHOPIFY_FLAG_STORE_PASSWORD" or k.strip() == "STORE_PASSWORD":
            env["SHOPIFY_FLAG_STORE_PASSWORD"] = v.strip().strip("'\"")
    cmd = ["shopify", "theme", "dev", "--store", STORE, "--path", str(ROOT / "theme"), "--port", "9292", "--no-color", "--no-input"]
    if "--theme" in sys.argv:
        cmd += ["--theme", sys.argv[sys.argv.index("--theme") + 1]]
    log = deque(maxlen=20)
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
    import threading
    threading.Thread(target=lambda: [log.append(l.rstrip()) for l in proc.stdout], daemon=True).start()
    try:
        fails, rows = run(proc, log)
    finally:
        # ponytail: killpg can raise EPERM under a sandbox; fall back to terminate/kill so the port is always freed
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except OSError:
            proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    print(f"{'route':28} {'w':5} {'status':6} {'links':5} {'hover':6} result")
    for r in rows:
        print(f"{r[0]:28} {r[1]:<5} {r[2]:<6} {r[3]:<5} {r[4]:6} {r[5]}")
    print("ALL PASS" if not fails else "FAIL: " + " | ".join(fails))
    sys.exit(1 if fails else 0)


def run(proc, log):
    up = False
    for _ in range(75):
        try:
            up = urllib.request.urlopen(BASE + "/", timeout=5).status == 200
        except Exception:
            pass
        if up or proc.poll() is not None:
            break
        time.sleep(2)
    if not up:
        return ["dev server never returned 200; last log: " + " / ".join(log)], []
    import json
    try:
        prods = json.load(urllib.request.urlopen(BASE + "/products.json", timeout=20))["products"]
    except Exception:
        prods = []
    routes = list(ROUTES)
    if prods:
        routes.insert(7, f"/products/{prods[0]['handle']}")
    else:
        print("note: store has no products; product page + /products/* links skipped")
    SHOTS.mkdir(parents=True, exist_ok=True)
    fails, rows, seen = [], [], set()
    css, js = (ROOT / "theme/assets/site.css").read_text(), (ROOT / "theme/assets/site.js").read_text()
    if not re.search(r"\.hero::after\{[^}]*pointer-events:none", css) or "touchend" not in js:
        fails.append("hero tap-through: .hero::after needs pointer-events:none and site.js needs the touchend autoplay kick")
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for route in routes:
            for w, h in VIEWPORTS:
                ctx = browser.new_context(viewport={"width": w, "height": h})
                pg = ctx.new_page()
                errs, warns = [], []
                pg.on("pageerror", lambda e: errs.append(f"page error {e}"))
                pg.on("console", lambda m: m.type == "error" and warns.append(m.text[:80]))
                resp = pg.goto(BASE + route, wait_until="load")
                status = resp.status if resp else 0
                want = 404 if "does-not-exist" in route else 200
                if status != want:
                    m = re.match(r"/pages/(\w+)$", route)
                    errs.append(f'PAGE MISSING in admin: create a page titled "{m[1].capitalize()}" (handle {m[1]})' if m and status == 404 else f"status {status}")
                pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
                pg.wait_for_timeout(500)
                y = 0
                while y < pg.evaluate("document.documentElement.scrollHeight"):  # scroll so .reveal fires
                    y += 500
                    pg.evaluate(f"scrollTo(0,{y})")
                    pg.wait_for_timeout(60)
                pg.evaluate("scrollTo(0,0)")
                pg.wait_for_timeout(900)
                over = pg.evaluate("document.documentElement.scrollWidth - innerWidth")
                if over > 0:
                    errs.append(f"horizontal overflow {over}px")
                broken = pg.evaluate("[...document.images].filter(i=>!i.src.startsWith('data:')&&!i.naturalWidth).map(i=>i.getAttribute('src'))")
                if broken:
                    errs.append(f"broken images {broken}")
                hrefs = {urldefrag(a)[0] for a in pg.evaluate("[...document.querySelectorAll('a[href^=\"/\"]')].map(a=>a.getAttribute('href'))") if a.startswith("/") and not a.startswith("//")}
                for hr in sorted(hrefs - seen):
                    seen.add(hr)
                    if hr.startswith("/products/") and not prods:
                        continue
                    if ctx.request.get(BASE + hr).status == 404:
                        errs.append(f"link 404 {hr}")
                hov = "-"
                if route == "/" and w == 1440 and pg.query_selector("main .lamp img"):
                    before = pg.evaluate("getComputedStyle(document.querySelector('main .lamp img')).filter")
                    pg.hover("main .lamp")
                    pg.wait_for_timeout(800)
                    hov = "off" if pg.evaluate("getComputedStyle(document.querySelector('main .lamp img')).filter") == before else "LIT"
                    if hov == "LIT":
                        errs.append("lamp still lights on hover")
                pg.mouse.move(0, 0)
                slug = route.strip("/").replace("/", "-").replace("?", "-").replace("=", "-") or "home"
                pg.screenshot(path=str(SHOTS / f"{slug}-{w}.png"), full_page=True)
                if warns:
                    print(f"WARN {route}@{w}: {len(warns)} console errors, e.g. {warns[0]}")
                rows.append((route, w, status, len(hrefs), hov, "ok" if not errs else "; ".join(errs)))
                fails += [f"{route}@{w}: {e}" for e in errs]
                ctx.close()
        browser.close()
    return fails, rows


if __name__ == "__main__":
    main()
