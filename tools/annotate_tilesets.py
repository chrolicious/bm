"""Zoom each tileset 4x, draw a red grid, number each 8x8 tile."""
from PIL import Image, ImageDraw
import os

SCALE = 4
ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC  = os.path.join(ROOT, "gfx", "pokecrystal-src", "gfx", "tilesets")
OUT  = os.path.join(ROOT, "gfx")

names = ["house", "facility", "dark_cave", "underground", "players_room", "park", "cave"]

for name in names:
    path = os.path.join(SRC, f"{name}.png")
    if not os.path.exists(path):
        print(f"SKIP {name}")
        continue
    img = Image.open(path).convert("RGB")
    w, h = img.size
    scaled = img.resize((w * SCALE, h * SCALE), Image.NEAREST)
    draw = ImageDraw.Draw(scaled)
    tw = w // 8
    th = h // 8
    for tx in range(tw + 1):
        draw.line([(tx*8*SCALE, 0), (tx*8*SCALE, h*SCALE-1)], fill=(255,0,0))
    for ty in range(th + 1):
        draw.line([(0, ty*8*SCALE), (w*SCALE-1, ty*8*SCALE)], fill=(255,0,0))
    for ty in range(th):
        for tx in range(tw):
            idx = ty * tw + tx
            draw.text((tx*8*SCALE+1, ty*8*SCALE+1), str(idx), fill=(255,0,0))
    out = os.path.join(OUT, f"annot_{name}.png")
    scaled.save(out)
    print(f"{name}: {tw}x{th} tiles ({tw*th} total) -> {out}")
