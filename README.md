# Light + Form Concepts - website MVP

Static draft site for Light + Form Concepts (Balestier Road, Singapore). Two variants, identical except fonts:
`/` (V1) and `/v2/` (V2, Bedrock typography). Placeholders are marked with a dotted amber `.ph` tag.

- Preview: `python3 -m http.server 8812`, then open `http://127.0.0.1:8812/` and `/v2/`
- Rebuild V2 after any HTML change: `python3 scripts/build_v2.py`
- Check (needs Python Playwright): `python3 scripts/check.py` - must end `ALL PASS`; screenshots land in `research/screens/`
- Deploy to GitHub Pages: `./deploy.sh` (runs the check first, needs a clean committed tree)

Layout: `css/` (tokens, fonts, base, components), `js/site.js`, `assets/`, flat `*.html` pages.
Fonts: `css/fonts.css` (V1) vs `css/fonts-v2.css` (V2); licensed files can be added later via the commented `@font-face` hooks.
