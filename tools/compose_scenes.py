"""
Compose 160x144 (20x18 tile) scene images from pokecrystal tilesets.
Each scene is a proper room layout rather than a raw atlas repeat.
Output PNGs go to gfx/scenes/ and are then fed to png2asset.

Coordinate system: col/row index 8x8 tiles inside the source PNG.
"""
from PIL import Image
import os, subprocess, sys

ROOT  = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC   = os.path.join(ROOT, "gfx", "pokecrystal-src", "gfx", "tilesets")
OUT   = os.path.join(ROOT, "gfx", "scenes")
BG    = os.path.join(ROOT, "src", "bg")
TOOLS = os.path.join(ROOT, "tools", "gbdk", "bin")
os.makedirs(OUT, exist_ok=True)
os.makedirs(BG, exist_ok=True)

WHITE = (255, 255, 255)

# GBC palette levels used in this project: white, light-gray, dark-gray, black
_LEVELS = [255, 170, 85, 0]

def _snap(v):
    """Snap a 0-255 value to the nearest of our 4 GBC palette levels."""
    return min(_LEVELS, key=lambda l: abs(v - l))

def to_gbpal(img):
    """Convert a PIL image to grayscale quantized to exactly our 4 GBC levels."""
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
    """Return 8x8 PIL image for tile at (col, row) in the source."""
    x, y = col * 8, row * 8
    return img.crop((x, y, x + 8, y + 8))

def new_scene(bg=WHITE):
    return Image.new("RGB", (160, 144), bg)

def fill(canvas, t, x1, y1, x2, y2):
    """Tile a single 8x8 tile across the rectangle [x1,x2) x [y1,y2) in tile coords."""
    for row in range(y1, y2):
        for col in range(x1, x2):
            canvas.paste(t, (col * 8, row * 8))

def row_from_src(canvas, src, src_row, scene_row, src_cols=16, scene_cols=20):
    """Copy one row from source tileset into a scene row, wrapping cols."""
    for sc in range(scene_cols):
        canvas.paste(tile(src, sc % src_cols, src_row), (sc * 8, scene_row * 8))

def rows_from_src(canvas, src, mapping, src_cols=16, scene_cols=20):
    """mapping = {scene_row: src_row, ...}  or list [(scene_row, src_row)]"""
    if isinstance(mapping, dict):
        mapping = mapping.items()
    for scene_row, src_row in mapping:
        row_from_src(canvas, src, src_row, scene_row, src_cols, scene_cols)

# ── load tilesets ────────────────────────────────────────────────────────────
fac  = load("facility")        # school/lab interior  (16x6 tiles)
hse  = load("house")           # home interior        (16x6 content rows)
cave = load("dark_cave")       # dark cave            (16x6 tiles)
ugnd = load("underground")     # underground/club     (16x12, rows 4-6 = diamond floor)
prm  = load("players_room")    # player bedroom       (16x6 tiles)
park = load("park")            # outdoor / garden     (16x12 tiles)

# ── precompute frequently-used tiles ─────────────────────────────────────────
# White / blank sky
t_sky   = Image.new("RGB", (8, 8), WHITE)
# facility checkered floor (col 0, row 0)
t_fflr  = tile(fac, 0, 0)
# facility floor variant (col 1, row 0)
t_fflr2 = tile(fac, 1, 0)

# ── Scene 1: Classroom ────────────────────────────────────────────────────────
#   facility.png layout:
#     row 5: left side has plainer wall tiles -> use as ceiling/top wall
#     rows 3-4: mid-facility elements (shelves, frames) -> wall area
#     rows 1-2: computer stations / desk equipment -> desk rows
#     row 0: checkered floor tiles
def scene_classroom():
    s = new_scene()
    # Ceiling / top wall trim
    row_from_src(s, fac, 5, 0)
    # Wall above blackboard (repeating wall row from fac row 4)
    row_from_src(s, fac, 4, 1)
    # Blackboard area: 3 rows spanning cols 3..16, wall on sides
    for sr in range(2, 5):
        row_from_src(s, fac, 3, sr)
    # Wall below blackboard
    row_from_src(s, fac, 4, 5)
    # Floor/desk transition
    row_from_src(s, fac, 5, 6)
    # Two desk rows (equipment from rows 1-2 of facility)
    row_from_src(s, fac, 1, 7)
    row_from_src(s, fac, 2, 8)
    # Gap + second desk row
    row_from_src(s, fac, 0, 9)   # floor between desks
    row_from_src(s, fac, 1, 10)
    row_from_src(s, fac, 2, 11)
    # Floor rows (visible)
    for r in range(12, 14):
        row_from_src(s, fac, 0, r)
    # Hidden rows (under textbox, rows 14-17)
    for r in range(14, 18):
        row_from_src(s, fac, 0, r)
    return s

# ── Scene 2: Schoolyard ───────────────────────────────────────────────────────
#   park.png: rows 0-1 have sky+ground mix; rows 2-4 outdoor elements (trees, benches)
def scene_schoolyard():
    s = new_scene()
    # Open sky
    for r in range(4):
        fill(s, t_sky, 0, r, 20, r + 1)
    # School building top (park row 0 has building-like tiles on the right half)
    row_from_src(s, park, 0, 4)
    row_from_src(s, park, 1, 5)
    row_from_src(s, park, 2, 6)
    row_from_src(s, park, 3, 7)
    # Ground / grass rows
    for r in range(8, 14):
        row_from_src(s, park, r % 4 + 2, r)   # cycle park rows 2-5
    # Hidden
    for r in range(14, 18):
        row_from_src(s, park, 2, r)
    return s

# ── Scene 3: BWL Cave ─────────────────────────────────────────────────────────
#   dark_cave.png rows 0-1: rocky wall texture; rows 3-4: dark interior
def scene_bwl():
    s = new_scene((0, 0, 0))
    # Rocky ceiling
    for r in range(2):
        row_from_src(s, cave, r, r)
    # Dark cave interior
    for r in range(2, 12):
        row_from_src(s, cave, 3 + (r % 2), r)   # alternate rows 3 and 4
    # Rocky floor
    for r in range(12, 18):
        row_from_src(s, cave, 1 - (r % 2), r)
    return s

# ── Scene 4: Living Room ──────────────────────────────────────────────────────
#   house.png rows 0-5 have content (furniture, walls, TV, bookshelf)
def scene_living_room():
    s = new_scene()
    # Top wall / ceiling
    row_from_src(s, hse, 0, 0)
    row_from_src(s, hse, 1, 1)
    # Wall with furniture on it (shelves, clock, picture)
    row_from_src(s, hse, 2, 2)
    row_from_src(s, hse, 3, 3)
    # Sofa / TV area
    row_from_src(s, hse, 4, 4)
    row_from_src(s, hse, 5, 5)
    row_from_src(s, hse, 4, 6)
    row_from_src(s, hse, 5, 7)
    # Floor
    for r in range(8, 14):
        row_from_src(s, hse, r % 2, r)     # alternate floor tiles from rows 0-1
    for r in range(14, 18):
        row_from_src(s, hse, 0, r)
    return s

# ── Scene 5: Spain Bar ────────────────────────────────────────────────────────
#   underground.png top rows for bar walls; rows 4-6 = diamond floor
def scene_spain_bar():
    s = new_scene()
    # Ceiling / bar wall top
    row_from_src(s, ugnd, 0, 0)
    row_from_src(s, ugnd, 1, 1)
    row_from_src(s, ugnd, 2, 2)
    # Bar counter row (row 3 of underground has counter-like elements)
    row_from_src(s, ugnd, 3, 3)
    # Diamond/tile floor from underground rows 4-6
    for r in range(4, 14):
        row_from_src(s, ugnd, 4 + (r % 3), r)
    for r in range(14, 18):
        row_from_src(s, ugnd, 4, r)
    return s

# ── Scene 6: Spain Bedroom ───────────────────────────────────────────────────
#   players_room.png has bed (rows 0-1), desk (rows 2-3), floor (rows 4-5)
def scene_spain_bedroom():
    s = new_scene()
    # Wall / ceiling
    row_from_src(s, prm, 4, 0)
    row_from_src(s, prm, 5, 1)
    # Bed (rows 0-1 of players_room have the bed graphic)
    row_from_src(s, prm, 0, 2)
    row_from_src(s, prm, 1, 3)
    row_from_src(s, prm, 0, 4)
    row_from_src(s, prm, 1, 5)
    # Floor
    for r in range(6, 14):
        row_from_src(s, prm, 4 + (r % 2), r)
    for r in range(14, 18):
        row_from_src(s, prm, 4, r)
    return s

# ── Scene 7: Aachen Club ─────────────────────────────────────────────────────
#   underground rows 0-3: dark club atmosphere; rows 4-6: diamond dance floor
def scene_aachen():
    s = new_scene((0, 0, 0))
    # Dark ceiling / walls
    for r in range(8):
        row_from_src(s, ugnd, r % 4, r)
    # Diamond club floor (underground rows 4-6)
    for r in range(8, 18):
        row_from_src(s, ugnd, 4 + (r % 3), r)
    return s

# ── Scene 8: Garden / The Ask ────────────────────────────────────────────────
#   open sky, hedge/trees from park, garden ground
def scene_ask():
    s = new_scene()
    # Sky
    for r in range(5):
        fill(s, t_sky, 0, r, 20, r + 1)
    # Trees / hedge
    row_from_src(s, park, 4, 5)
    row_from_src(s, park, 5, 6)
    row_from_src(s, park, 4, 7)
    # Garden ground
    for r in range(8, 14):
        row_from_src(s, park, 2 + (r % 3), r)
    for r in range(14, 18):
        row_from_src(s, park, 2, r)
    return s

# ── Generate scenes + run png2asset ─────────────────────────────────────────
png2asset = os.path.join(TOOLS, "png2asset.exe")

scenes = [
    ("classroom",      scene_classroom()),
    ("schoolyard",     scene_schoolyard()),
    ("bwl",            scene_bwl()),
    ("living_room",    scene_living_room()),
    ("spain_bar",      scene_spain_bar()),
    ("spain_bedroom",  scene_spain_bedroom()),
    ("aachen",         scene_aachen()),
    ("ask",            scene_ask()),
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
        # Inject #pragma bank 2 before BANKREF so data lands in ROM bank 2
        with open(c_out) as f:
            content = f.read()
        content = content.replace(
            "\nBANKREF(",
            "\n#pragma bank 2\nBANKREF(",
            1,
        )
        with open(c_out, "w") as f:
            f.write(content)
        import re
        m = re.search(r'const uint8_t \w+\[(\d+)\]', content)
        n = int(m.group(1)) // 16 if m else '?'
        print(f"  -> {c_out}  ({n} tiles)")
