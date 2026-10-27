#!/usr/bin/env python3
"""Cut-out lamp photo (white bg) -> revolved GLB with emissive shade + plain base (Shopify AR).
Usage: lamp_glb.py IMAGE --height-mm H --shade-frac F --out OUT.glb [--segments 64 --rows 96 --bg 235 --preview OUT.png]
Pure stdlib + Pillow. Y up, metres, lamp bottom at y=0, axis at x=z=0."""
import argparse, json, math, struct, sys
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("image"); ap.add_argument("--height-mm", type=float, required=True)
ap.add_argument("--shade-frac", type=float, required=True); ap.add_argument("--out", required=True)
ap.add_argument("--segments", type=int, default=64); ap.add_argument("--rows", type=int, default=96)
ap.add_argument("--bg", type=int, default=235); ap.add_argument("--preview")
a = ap.parse_args()

im = Image.open(a.image).convert("RGB"); W, H = im.size; px = im.load()
fg = lambda p: min(p) < a.bg
spans = {}  # y -> (left, right)
for y in range(H):
    xs = [x for x in range(W) if fg(px[x, y])]
    if len(xs) >= 3: spans[y] = (xs[0], xs[-1])
y0, y1 = min(spans), max(spans)
tot = sum(r - l for l, r in spans.values())
axis = sum((l + r) / 2 * (r - l) for l, r in spans.values()) / tot
# ponytail: rows with <3 px inside the bbox (rare gaps) reuse the nearest row's span
rad = []
for y in range(y0, y1 + 1):
    l, r = spans[min(spans, key=lambda k: abs(k - y))]
    rad.append(max(r - axis, axis - l))
rad = [max(1.0, sum(rad[max(0, i - 1):i + 2]) / len(rad[max(0, i - 1):i + 2])) for i in range(len(rad))]
n = a.rows
prof_px = []  # (image y, radius px), top -> bottom
for i in range(n):
    f = i / (n - 1) * (len(rad) - 1); k = int(f); t = f - k
    r = rad[k] * (1 - t) + rad[min(k + 1, len(rad) - 1)] * t
    prof_px.append((y0 + f, r))
bbox_h = y1 - y0 + 1
s = a.height_mm / bbox_h / 1000.0
prof = [((y1 + 1 - y) * s, r * s) for y, r in prof_px]  # (height m, radius m)
split = round(a.shade_frac * (n - 1))  # ring index of shade/base boundary (from top)

def mean_rgb(ya, yb):
    c = [0, 0, 0]; k = 0
    for y in range(int(ya), int(yb) + 1):
        for x in range(W):
            if y in spans and fg(px[x, y]):
                for q in range(3): c[q] += px[x, y][q]
                k += 1
    return [v / k for v in c]
lin = lambda v: ((v / 255 + 0.055) / 1.055) ** 2.4 if v / 255 > 0.04045 else v / 255 / 12.92
ysplit = prof_px[split][0]
sh = [min(255, v * 1.1) for v in mean_rgb(y0, ysplit)]
ba = mean_rgb(ysplit, y1)

S = a.segments
def prim(r0, r1, top, bot):
    P, N, UV, I = [], [], [], []
    for i in range(r0, r1 + 1):
        pa, pb = prof[max(i - 1, 0)], prof[min(i + 1, n - 1)]
        dy, dr = pb[0] - pa[0], pb[1] - pa[1]  # going down: dy < 0
        L = math.hypot(dy, dr) or 1
        nr, ny = -dy / L, dr / L
        for j in range(S + 1):
            t = 2 * math.pi * j / S
            P.append((prof[i][1] * math.cos(t), prof[i][0], prof[i][1] * math.sin(t)))
            N.append((nr * math.cos(t), ny, nr * math.sin(t)))
            UV.append((j / S, 1 - i / (n - 1)))
    for i in range(r1 - r0):
        for j in range(S):
            A = i * (S + 1) + j; B = A + 1; C = A + S + 1; D = C + 1
            I += [A, B, C, B, D, C]
    for ring, up, on in ((r0, 1, top), (r1, -1, bot)):
        if not on: continue
        c = len(P); y = prof[ring][0]; base = (ring - r0) * (S + 1)
        P.append((0, y, 0)); N.append((0, up, 0)); UV.append((.5, .5))
        for j in range(S + 1):
            p = P[base + j]; P.append(p); N.append((0, up, 0)); UV.append((.5 + .5 * math.cos(2 * math.pi * j / S), .5 + .5 * math.sin(2 * math.pi * j / S)))
        for j in range(S):
            I += [c, c + 2 + j, c + 1 + j] if up > 0 else [c, c + 1 + j, c + 2 + j]
    return P, N, UV, I

prims = [prim(0, split, True, False), prim(split, n - 1, False, True)]
blob = bytearray(); views = []; acc = []
def add(data, comp, typ, count, target, mm=None):
    while len(blob) % 4: blob.append(0)
    views.append({"buffer": 0, "byteOffset": len(blob), "byteLength": len(data), "target": target})
    blob.extend(data)
    d = {"bufferView": len(views) - 1, "componentType": comp, "count": count, "type": typ}
    if mm: d["min"], d["max"] = mm
    acc.append(d); return len(acc) - 1
jp = []
for mat, (P, N, UV, I) in enumerate(prims):
    fl = lambda seq: struct.pack(f"<{len(seq) * len(seq[0])}f", *[v for t in seq for v in t])
    mm = ([min(p[k] for p in P) for k in range(3)], [max(p[k] for p in P) for k in range(3)])
    jp.append({"attributes": {"POSITION": add(fl(P), 5126, "VEC3", len(P), 34962, mm),
                              "NORMAL": add(fl(N), 5126, "VEC3", len(N), 34962),
                              "TEXCOORD_0": add(fl(UV), 5126, "VEC2", len(UV), 34962)},
               "indices": add(struct.pack(f"<{len(I)}I", *I), 5125, "SCALAR", len(I), 34963), "material": mat, "mode": 4})
col = lambda c: [round(lin(v), 4) for v in c] + [1.0]
gj = {"asset": {"version": "2.0", "generator": "lightform lamp_glb"}, "extensionsUsed": ["KHR_materials_emissive_strength"],
      "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0}], "meshes": [{"primitives": jp}],
      "materials": [{"name": "shade", "pbrMetallicRoughness": {"baseColorFactor": col(sh), "roughnessFactor": 0.9, "metallicFactor": 0.0},
                     "emissiveFactor": [1.0, 0.86, 0.62], "extensions": {"KHR_materials_emissive_strength": {"emissiveStrength": 2.0}}},
                    {"name": "base", "pbrMetallicRoughness": {"baseColorFactor": col(ba), "roughnessFactor": 0.6, "metallicFactor": 0.0}}],
      "accessors": acc, "bufferViews": views, "buffers": [{"byteLength": len(blob)}]}
js = json.dumps(gj, separators=(",", ":")).encode(); js += b" " * (-len(js) % 4)
while len(blob) % 4: blob.append(0)
total = 12 + 8 + len(js) + 8 + len(blob)
open(a.out, "wb").write(struct.pack("<4sII", b"glTF", 2, total) + struct.pack("<I4s", len(js), b"JSON") + js + struct.pack("<I4s", len(blob), b"BIN\0") + bytes(blob))

if a.preview:
    pv = im.copy(); d = ImageDraw.Draw(pv)
    for sgn in (-1, 1):
        d.line([(axis + sgn * r, y) for y, r in prof_px], fill=(255, 0, 0), width=2)
    d.line([(0, ysplit), (W, ysplit)], fill=(0, 0, 255), width=2)
    pv.save(a.preview)

# self-check: re-open GLB
f = open(a.out, "rb").read()
assert f[:4] == b"glTF" and struct.unpack("<I", f[4:8])[0] == 2 and struct.unpack("<I", f[8:12])[0] == len(f), "bad header"
jl = struct.unpack("<I", f[12:16])[0]; assert f[16:20] == b"JSON"
j = json.loads(f[20:20 + jl]); o = 20 + jl
bl = struct.unpack("<I", f[o:o + 4])[0]; assert f[o + 4:o + 8] == b"BIN\0" and o + 8 + bl == len(f), "bad BIN chunk"
tris = sum(j["accessors"][p["indices"]]["count"] for p in j["meshes"][0]["primitives"]) // 3
pm = [j["accessors"][p["attributes"]["POSITION"]] for p in j["meshes"][0]["primitives"]]
lo = [min(m["min"][k] for m in pm) for k in range(3)]; hi = [max(m["max"][k] for m in pm) for k in range(3)]
h, w, dp = hi[1] - lo[1], hi[0] - lo[0], hi[2] - lo[2]
print(f"{a.out}: {len(f)} bytes, {tris} triangles, bbox x[{lo[0]:.4f},{hi[0]:.4f}] y[{lo[1]:.4f},{hi[1]:.4f}] z[{lo[2]:.4f},{hi[2]:.4f}] -> W {w:.4f} H {h:.4f} D {dp:.4f} m")
if abs(h - a.height_mm / 1000) > 0.005 * a.height_mm / 1000 or max(w, dp) > h * 1.5 or len(f) > 1_000_000:
    sys.exit("SELF-CHECK FAILED")
print("self-check OK")
