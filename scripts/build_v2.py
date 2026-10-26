#!/usr/bin/env python3
"""Mirror every top-level *.html into v2/ with asset paths pushed up a level and the V2 fonts sheet."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render(html: str) -> str:
    html = html.replace("css/fonts.css", "css/fonts-v2.css")
    return re.sub(r'(href="|src="|srcset="|url\()(css/|js/|assets/)', r"\1../\2", html)


def main() -> None:
    out = ROOT / "v2"
    out.mkdir(exist_ok=True)
    pages = sorted(ROOT.glob("*.html"))
    for stale in out.glob("*.html"):
        if not (ROOT / stale.name).exists():
            stale.unlink()
    for p in pages:
        (out / p.name).write_text(render(p.read_text()))
        print("wrote", f"v2/{p.name}")


if __name__ == "__main__":
    main()
