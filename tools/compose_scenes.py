"""
Compose 160x144 (20x18 tile) scene images from pokecrystal tilesets.
Each scene is a proper room layout rather than a raw atlas repeat.
Output PNGs go to gfx/scenes/ and are then fed to png2asset.

Coordinate system: col/row index 8x8 tiles inside the source PNG.
Sprites: 16x16px = 2x2 tiles. place_sprite(canvas, name, col, row).
"""
from PIL import Image
import os, subprocess, re

ROOT    = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC     = os.path.join(ROOT, "gfx", "pokecrystal-src", "gfx", "tilesets")
SPRITES = os.path.join(ROOT, "gfx", "pokecrystal-src", "gfx", "sprites")
OUT     = os.path.join(ROOT, "gfx", "scenes")
BG      = os.path.join(ROOT, "src", "bg")
TOOLS   = os.path.join(ROOT, "tools", "gbdk", "bin")
os.makedirs(OUT, exist_ok=True)
os.makedirs(BG, exist_ok=True)

WHITE = (255, 255, 255)

_LEVELS = [255, 170, 85, 0]

def _snap(v):
    return min(_LEVELS, key=lambda l: abs(v - l))

def to_gbpal(img):
    grey = img.convert("L")
    px   = grey.load()
    w, h = grey.size
    for y in range(h):
        for x in range(w):
            px[x, y] = _snap(px[x, y])
    return grey.convert("RGB")

def load(name):
    return Image.open(os.path.join(SRC, f"{name}.png")).convert("RGB")

def tile(img, col, row):
    x, y = col * 8, row * 8
    return img.crop((x, y, x + 8, y + 8))

def new_scene(bg=WHITE):
    return Image.new("RGB", (160, 144), bg)

def fill(canvas, t, x1, y1, x2, y2):
    for row in range(y1, y2):
        for col in range(x1, x2):
            canvas.paste(t, (col * 8, row * 8))

def row_from_src(canvas, src, src_row, scene_row, src_cols=16, scene_cols=20):
    for sc in range(scene_cols):
        canvas.paste(tile(src, sc % src_cols, src_row), (sc * 8, scene_row * 8))

def rows_from_src(canvas, src, mapping, src_cols=16, scene_cols=20):
    if isinstance(mapping, dict):
        mapping = mapping.items()
    for scene_row, src_row in mapping:
        row_from_src(canvas, src, src_row, scene_row, src_cols, scene_cols)

# ── Sprite helpers ────────────────────────────────────────────────────────────
# Each sprite sheet is 16px wide x 96px tall = six 16x16 frames:
#   frame 0: facing down  (toward player)
#   frame 2: facing up    (away from player)
#   frame 4: facing side  (left; flip horizontally for right)
FACE_DOWN = 0
FACE_UP   = 2
FACE_SIDE = 4

def load_sprite(name, frame=FACE_DOWN, flip=False):
    """Return a 16x16 PIL image for one frame of a pokecrystal overworld sprite."""
    img = Image.open(os.path.join(SPRITES, f"{name}.png")).convert("RGB")
    spr = img.crop((0, frame * 16, 16, frame * 16 + 16))
    if flip:
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    return spr

def place_sprite(canvas, name, col, row, frame=FACE_DOWN, flip=False):
    """Paste a 16x16 sprite at tile grid (col, row); white pixels are transparent."""
    spr = to_gbpal(load_sprite(name, frame, flip))
    mask = spr.convert("L").point(lambda p: 0 if p >= 250 else 255)
    canvas.paste(spr, (col * 8, row * 8), mask)

# ── load tilesets ─────────────────────────────────────────────────────────────
fac  = load("facility")
hse  = load("house")
cave = load("dark_cave")
ugnd = load("underground")
prm  = load("players_room")
park = load("park")

t_sky   = Image.new("RGB", (8, 8), WHITE)
t_fflr  = tile(fac, 0, 0)
t_fflr2 = tile(fac, 1, 0)

# ── Scene 1: Classroom ────────────────────────────────────────────────────────
def scene_classroom():
    s = new_scene()
    row_from_src(s, fac, 5, 0)
    row_from_src(s, fac, 4, 1)
    for sr in range(2, 5):
        row_from_src(s, fac, 3, sr)
    row_from_src(s, fac, 4, 5)
    row_from_src(s, fac, 5, 6)
    row_from_src(s, fac, 1, 7)
    row_from_src(s, fac, 2, 8)
    row_from_src(s, fac, 0, 9)
    row_from_src(s, fac, 1, 10)
    row_from_src(s, fac, 2, 11)
    for r in range(12, 18):
        row_from_src(s, fac, 0, r)
    # Teacher at the board, facing it
    place_sprite(s, "teacher",   col=9,  row=4, frame=FACE_UP)
    # Students at desks
    place_sprite(s, "lass",      col=2,  row=9, frame=FACE_DOWN)
    place_sprite(s, "youngster", col=7,  row=9, frame=FACE_DOWN)
    place_sprite(s, "lass",      col=13, row=9, frame=FACE_DOWN)
    place_sprite(s, "youngster", col=16, row=9, frame=FACE_DOWN)
    return s

# ── Scene 2: Schoolyard ───────────────────────────────────────────────────────
# Managed via TileMap Studio + import_level_json.py — not regenerated here.

# ── Scene 3: BWL Cave ─────────────────────────────────────────────────────────
def scene_bwl():
    s = new_scene((0, 0, 0))
    for r in range(2):
        row_from_src(s, cave, r, r)
    for r in range(2, 12):
        row_from_src(s, cave, 3 + (r % 2), r)
    for r in range(12, 18):
        row_from_src(s, cave, 1 - (r % 2), r)
    return s

# ── Scene 4: Living Room ──────────────────────────────────────────────────────
def scene_living_room():
    s = new_scene()
    row_from_src(s, hse, 0, 0)
    row_from_src(s, hse, 1, 1)
    row_from_src(s, hse, 2, 2)
    row_from_src(s, hse, 3, 3)
    row_from_src(s, hse, 4, 4)
    row_from_src(s, hse, 5, 5)
    row_from_src(s, hse, 4, 6)
    row_from_src(s, hse, 5, 7)
    for r in range(8, 18):
        row_from_src(s, hse, r % 2, r)
    # Four friends on the sofa / standing
    place_sprite(s, "rival",     col=1,  row=5, frame=FACE_DOWN)
    place_sprite(s, "gentleman", col=6,  row=5, frame=FACE_DOWN)
    place_sprite(s, "kris",      col=11, row=5, frame=FACE_DOWN)
    place_sprite(s, "chris",     col=16, row=5, frame=FACE_DOWN)
    return s

# ── Scene 5: Spain Bar ────────────────────────────────────────────────────────
def scene_spain_bar():
    s = new_scene()
    row_from_src(s, ugnd, 0, 0)
    row_from_src(s, ugnd, 1, 1)
    row_from_src(s, ugnd, 2, 2)
    row_from_src(s, ugnd, 3, 3)
    for r in range(4, 18):
        row_from_src(s, ugnd, 4 + (r % 3), r)
    # Waitresses behind the bar counter
    place_sprite(s, "beauty", col=3,  row=2, frame=FACE_DOWN)
    place_sprite(s, "beauty", col=13, row=2, frame=FACE_DOWN)
    # Tobi and Michel at the bar
    place_sprite(s, "kris",  col=6,  row=6, frame=FACE_UP)
    place_sprite(s, "chris", col=11, row=6, frame=FACE_UP)
    return s

# ── Scene 6: Spain Bedroom ────────────────────────────────────────────────────
def scene_spain_bedroom():
    s = new_scene()
    row_from_src(s, prm, 4, 0)
    row_from_src(s, prm, 5, 1)
    row_from_src(s, prm, 0, 2)
    row_from_src(s, prm, 1, 3)
    row_from_src(s, prm, 0, 4)
    row_from_src(s, prm, 1, 5)
    for r in range(6, 18):
        row_from_src(s, prm, 4 + (r % 2), r)
    # Tobi and her dad
    place_sprite(s, "kris",   col=5,  row=5, frame=FACE_DOWN)
    place_sprite(s, "gramps", col=12, row=5, frame=FACE_DOWN)
    return s

# ── Scene 7: Aachen Club ──────────────────────────────────────────────────────
def scene_aachen():
    s = new_scene((0, 0, 0))
    for r in range(8):
        row_from_src(s, ugnd, r % 4, r)
    for r in range(8, 18):
        row_from_src(s, ugnd, 4 + (r % 3), r)
    # Crowd on the dance floor
    place_sprite(s, "youngster",   col=1,  row=5, frame=FACE_SIDE)
    place_sprite(s, "lass",        col=5,  row=4, frame=FACE_SIDE, flip=True)
    place_sprite(s, "cooltrainer_m", col=14, row=5, frame=FACE_SIDE)
    place_sprite(s, "cooltrainer_f", col=17, row=4, frame=FACE_SIDE, flip=True)
    # Tobi and Michel
    place_sprite(s, "kris",  col=8,  row=7, frame=FACE_DOWN)
    place_sprite(s, "chris", col=12, row=7, frame=FACE_DOWN)
    return s

# ── Scene 8: Garden / The Ask ─────────────────────────────────────────────────
def scene_ask():
    s = new_scene()
    for r in range(5):
        fill(s, t_sky, 0, r, 20, r + 1)
    row_from_src(s, park, 4, 5)
    row_from_src(s, park, 5, 6)
    row_from_src(s, park, 4, 7)
    for r in range(8, 18):
        row_from_src(s, park, 2 + (r % 3), r)
    # Tobi and Michel in the garden
    place_sprite(s, "kris",  col=7,  row=8, frame=FACE_DOWN)
    place_sprite(s, "chris", col=12, row=8, frame=FACE_DOWN)
    return s

# ── Generate scenes + run png2asset ──────────────────────────────────────────
png2asset = os.path.join(TOOLS, "png2asset.exe")

scenes = [
    ("classroom",     scene_classroom()),
    # schoolyard: managed via TileMap Studio + import_level_json.py
    ("bwl",           scene_bwl()),
    ("living_room",   scene_living_room()),
    ("spain_bar",     scene_spain_bar()),
    ("spain_bedroom", scene_spain_bedroom()),
    ("aachen",        scene_aachen()),
    ("ask",           scene_ask()),
]

for name, img in scenes:
    png_path = os.path.join(OUT, f"{name}.png")
    img = to_gbpal(img)
    img.save(png_path)
    print(f"Saved {png_path}")

    c_out = os.path.join(BG, f"scene_{name}.c")
    cmd = [
        png2asset, png_path,
        "-map", "-use_map_attributes",
        "-bpp", "2",
        "-max_palettes", "1",
        "-tile_origin", "104",
        "-o", c_out,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
    else:
        with open(c_out) as f:
            content = f.read()
        content = content.replace("\nBANKREF(", "\n#pragma bank 2\nBANKREF(", 1)
        with open(c_out, "w") as f:
            f.write(content)
        m = re.search(r'const uint8_t \w+\[(\d+)\]', content)
        n = int(m.group(1)) // 16 if m else '?'
        print(f"  -> {c_out}  ({n} tiles)")
