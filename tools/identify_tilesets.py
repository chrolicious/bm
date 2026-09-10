"""
Find the correct tilesetId -> tileset mapping by sampling specific tiles
that are visually identifiable in the editor screenshot.

The top 4 rows are all tile (11,4) from ID 1784572843253 and appear DARK
in the screenshot. We find which tileset has the darkest pixel there.
"""
import json, base64, io
from PIL import Image

with open(r'C:\Users\epe_m\Downloads\level.json') as f:
    level = json.load(f)

tilesets = level['tilesets']
TS = 16

def decode(ts):
    b64 = ts['data'].split(',', 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert('L')

images = [decode(ts) for ts in tilesets]

def brightness(img, tx, ty):
    x0, y0 = tx * TS, ty * TS
    if x0 + TS > img.width or y0 + TS > img.height:
        return None
    crop = img.crop((x0, y0, x0 + TS, y0 + TS))
    return sum(crop.getdata()) / (TS * TS)

# Key diagnostic tiles from the layer data
checks = [
    # (id,        tx, ty,  description)
    (1784572843253, 11, 4, "rows 0-3 fill -- should be DARK (sky/background)"),
    (1784573750916, 14, 8, "building facade top-right"),
    (1784573750916, 10, 7, "building detail"),
    (1784573400361,  2, 6, "ground/floor tile"),
    (1784573400361,  0, 9, "lower ground"),
    (1784573550212,  6, 3, "accent element"),
]

for tid, tx, ty, desc in checks:
    print(f"\nID {tid}  tile({tx},{ty})  [{desc}]")
    results = []
    for i, (ts, img) in enumerate(zip(tilesets, images)):
        b = brightness(img, tx, ty)
        if b is not None:
            results.append((b, i, ts['name']))
    # show all, marking darkest and brightest
    results.sort()
    for b, i, name in results:
        marker = " <-- DARKEST" if b == results[0][0] else (" <-- BRIGHTEST" if b == results[-1][0] else "")
        print(f"  [{i}] {name:30s}  {b:6.1f}{marker}")
