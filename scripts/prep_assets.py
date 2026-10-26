"""Copy the client's photos from research/ into assets/img with kebab names, resized to <=1800px wide, JPEG q84.
Run: ~/.venvs/automation/bin/python scripts/prep_assets.py  (idempotent)"""
import os, re, glob
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = {
 'research/lightpro/img': None,
 'research/instagram/storefront-hero-placeholder.jpg': 'hero-storefront.jpg',
}
RENAME = {
 '310261_lisa_270_450_brass': 'innolux-lisa-brass.jpg', '310508_Bulbo-3': 'innolux-bulbo.jpg', '310508_Bulbo_interior': 'innolux-bulbo-interior.jpg',
 '321700_alma_table_interior': 'innolux-alma-table.jpg', '600-Coral-Red': 'trubridge-coral-red.jpg', '733000H_Candeo_grey_interi': 'innolux-candeo-grey.jpg',
 'Coral-Natural-Close-Up': 'trubridge-coral-natural-closeup.jpg', 'Coral-in-Nature': 'trubridge-coral-in-nature.jpg', 'Corals-natural-Private-Res': 'trubridge-corals-residence.jpg',
 'Guok-Ave-1': 'project-guok-avenue.jpg', 'Leonie-Hill-6': 'project-leonie-hill.jpg', 'PV1': 'project-parc-vera-rings.jpg', 'PV6': 'project-parc-vera-stars.jpg',
 'SL2': 'project-sim-lian.jpg', 'Madison_SMA301-N-WH1S_Livi': 'madison-wall-lights.jpg', 'RenoBackdrop': 'service-renovation.png', 'curtainbanner': 'service-curtains.jpg',
 'servicebanner': 'service-lighting.jpg', 'wirebanner': 'service-electrical.jpg', 'Crystal-Palace': 'swarovski-crystal-palace.png', 'Milano-500x400-1': 'schonbek-milano.jpg',
 'PHOTO-2020-05-11-14-11-33': 'swarovski-crystal-hand.jpg', 'aboutpage1': 'swarovski-crystal-rain.jpg', 'SwarovskiLighting_ALP-2_10': 'swarovski-authorized-partner.png',
}
out = os.path.join(ROOT, 'assets/img'); os.makedirs(out, exist_ok=True)
files = glob.glob(os.path.join(ROOT, 'research/lightpro/img/*/*')) + [os.path.join(ROOT, 'research/instagram/storefront-hero-placeholder.jpg')]
done = []
for f in files:
    base = os.path.splitext(os.path.basename(f))[0]
    base = re.sub(r'-scaled$', '', base)
    if 'payments' in base: continue
    name = RENAME.get(base[:26]) or RENAME.get(base) or ('hero-storefront.jpg' if 'storefront' in base else None)
    if not name:
        for k, v in RENAME.items():
            if base.startswith(k): name = v; break
    if not name: print('skip', base); continue
    dst = os.path.join(out, name)
    if os.path.exists(dst): done.append(name); continue
    im = Image.open(f)
    if im.width > 1800: im = im.resize((1800, int(1800 * im.height / im.width)), Image.LANCZOS)
    if name.endswith('.png'): im.save(dst, optimize=True)
    else: im.convert('RGB').save(dst, quality=84, optimize=True)
    done.append(name)
print(len(done), 'assets'); print('\n'.join(sorted(set(done))))
