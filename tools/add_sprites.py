"""
Overlay overworld sprites onto an existing scene PNG and re-run png2asset.

Usage:
    python tools/add_sprites.py <scene_name>

Example:
    python tools/add_sprites.py classroom

Reads  gfx/scenes/<scene_name>.png
Writes gfx/scenes/<scene_name>.png  (in-place, with sprites composited)
       src/bg/scene_<scene_name>.c
"""

import sys, os, re, subprocess
from PIL import Image

ROOT    = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SPRITES = os.path.join(ROOT, "gfx", "pokecrystal-src", "gfx", "sprites")
TOOLS   = os.path.join(ROOT, "tools", "gbdk", "bin")

FACE_DOWN = 0
FACE_UP   = 1
FACE_SIDE = 4

_LEVELS = [255, 170, 85, 0]
def _snap(v): return min(_LEVELS, key=lambda l: abs(v - l))
def _to_gbpal(img):
    grey = img.convert("L")
    px = grey.load()
    for y in range(grey.height):
        for x in range(grey.width):
            px[x, y] = _snap(px[x, y])
    return grey.convert("RGB")

def place_sprite(canvas, name, col, row, frame=FACE_DOWN, flip=False):
    img = Image.open(os.path.join(SPRITES, f"{name}.png")).convert("RGB")
    spr = img.crop((0, frame * 16, 16, frame * 16 + 16))
    if flip:
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    spr = _to_gbpal(spr)
    mask = spr.convert("L").point(lambda p: 0 if p >= 250 else 255)
    canvas.paste(spr, (col * 8, row * 8), mask)

# col/row are in 8px tile units; sprites are 16x16px (2x2 tiles)
SCENE_SPRITES = {
    "bwl": [
        ("chris",        1, 12, FACE_UP, False),  # Michel
        ("kris",         3, 12, FACE_UP, False),  # Tobi
        ("cooltrainer_m",5, 12, FACE_UP, False),  # Friets
        ("beauty",       7, 12, FACE_UP, False),  # Ayaro
        ("gentleman",    9, 12, FACE_UP, False),  # Aerendil
        ("rocker",      11, 12, FACE_UP, False),  # Aronian
        ("fisher",      13, 12, FACE_UP, False),  # Gerrit
        ("super_nerd",  15, 12, FACE_UP, False),  # Divinity
    ],
    "classroom": [
        ("teacher",   8,  3, FACE_DOWN, False),  # teacher below whiteboard, facing class
        ("chris",     4,  7, FACE_UP, False),  # Michel, front desk (facing north)
        ("lass",      8,  7, FACE_UP, False),  # classmate front row
        ("youngster", 14, 7, FACE_UP, False),  # classmate front row
        ("youngster", 16, 7, FACE_UP, False),  # classmate front row
        ("lass",      4,  12, FACE_UP, False),  # classmate mid row
        ("youngster", 8,  12, FACE_UP, False),  # classmate mid row
        ("lass",      14, 12, FACE_UP, False),  # classmate mid row
        ("kris",      16, 16, FACE_UP, False),  # Tobi, back-right (facing north)
    ],
}

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    scene_name = sys.argv[1]
    sprites = SCENE_SPRITES.get(scene_name)
    if not sprites:
        print(f"No sprites defined for scene '{scene_name}'")
        sys.exit(1)

    png_path = os.path.join(ROOT, "gfx", "scenes", f"{scene_name}.png")
    canvas = Image.open(png_path).convert("RGB")
    print(f"Loaded {png_path}  ({canvas.size})")

    for entry in sprites:
        place_sprite(canvas, *entry)
        print(f"  placed {entry[0]} at ({entry[1]},{entry[2]})")

    canvas = _to_gbpal(canvas)
    canvas.save(png_path)
    print(f"Saved {png_path}")

    c_out     = os.path.join(ROOT, "src", "bg", f"scene_{scene_name}.c")
    png2asset = os.path.join(TOOLS, "png2asset.exe")
    cmd = [png2asset, png_path, "-map", "-use_map_attributes",
           "-bpp", "2", "-max_palettes", "1", "-tile_origin", "104", "-o", c_out]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr.strip()}")
        sys.exit(1)

    with open(c_out) as f:
        content = f.read()
    content = content.replace("\nBANKREF(", "\n#pragma bank 2\nBANKREF(", 1)
    with open(c_out, "w") as f:
        f.write(content)

    m = re.search(r'const uint8_t \w+\[(\d+)\]', content)
    n = int(m.group(1)) // 16 if m else '?'
    print(f"  -> {c_out}  ({n} tiles)")
    if isinstance(n, int) and n > 152:
        print(f"  WARNING: {n} tiles exceeds 152 tile budget!")

if __name__ == "__main__":
    main()
