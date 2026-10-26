#!/usr/bin/env bash
# Deploy the Light + Form Concepts MVP to GitHub Pages (dethok/lightform-site, branch main, root).
# Preconditions: scripts/check.py ALL PASS (run here); tree committed. Done = the live index.html hash equals the local one.
set -euo pipefail
cd "$(dirname "$0")"
REPO=dethok/lightform-site
URL=https://dethok.com/lightform-site/
[ -z "$(git status --porcelain)" ] || { echo "uncommitted changes — commit first"; exit 1; }
# precondition: scripts/check.py must pass (builds v2 first)
python3 scripts/build_v2.py >/dev/null
"${PYTHON:-$HOME/.venvs/automation/bin/python}" scripts/check.py | tail -1 | grep -q "^ALL PASS" || { echo "scripts/check.py did not pass"; exit 1; }
git push -u origin main
gh api -X POST "repos/$REPO/pages" -f build_type=legacy -f 'source[branch]=main' -f 'source[path]=/' >/dev/null 2>&1 || true
want=$(shasum -a 256 index.html | cut -c1-16)
for i in $(seq 1 40); do
  got=$(curl -fsSL "$URL" 2>/dev/null | shasum -a 256 | cut -c1-16 || true)
  if [ "$got" = "$want" ]; then echo "LIVE $URL ($want) at $(date '+%H:%M:%S')"; exit 0; fi
  sleep 10
done
echo "NOT LIVE after 400 s (want $want, got ${got:-none})"; exit 1
