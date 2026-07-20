"""
Convert a level.json tile map (20x18, tileSize 16) to a 160x144 scene PNG
and run it through png2asset to produce a GBDK .c file.

Usage:
    python tools/import_level_json.py <level.json> <scene_name>

Example:
    python tools/import_level_json.py C:/Users/epe_m/Downloads/level.json schoolyard

The scene_name must match an existing entry in scenes.h (e.g. "schoolyard").
Output: gfx/scenes/<scene_name>.png and src/bg/scene_<scene_name>.c
"""

import json, sys, os, base64, io, re, subprocess
from PIL import Image

ROOT    = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS   = os.path.join(ROOT, "tools", "gbdk", "bin")
SPRITES = os.path.join(ROOT, "gfx", "pokecrystal-src", "gfx", "sprites")

FACE_DOWN = 0
FACE_UP   = 2
FACE_SIDE = 4

def _snap(v):
    levels = [255, 170, 85, 0]
    return min(levels, key=lambda l: abs(v - l))

def _to_gbpal(img):
    grey = img.convert("L")
    px = grey.load()
    for y in range(grey.height):
        for x in range(grey.width):
            px[x, y] = _snap(px[x, y])
    return grey.convert("RGB")

def place_sprite(canvas, name, col, row, frame=FACE_DOWN, flip=False):
    """Paste a 16x16 overworld sprite at tile grid (col, row); white = transparent."""
    img = Image.open(os.path.join(SPRITES, f"{name}.png")).convert("RGB")
    spr = img.crop((0, frame * 16, 16, frame * 16 + 16))
    if flip:
        spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    spr = _to_gbpal(spr)
    mask = spr.convert("L").point(lambda p: 0 if p >= 250 else 255)
    canvas.paste(spr, (col * 8, row * 8), mask)

# Sprites to place per scene name
SCENE_SPRITES = {
    "schoolyard": [
        ("chris",     10,  7, FACE_SIDE, True),   # Michel facing right (into group)
        ("kris",      12,  7, FACE_SIDE, False),   # Tobi facing left (into group)
        ("youngster", 11,  9, FACE_UP,   False),   # student in front, facing up toward group
        ("lass",      13,  9, FACE_SIDE, False),   # student beside, facing left
    ],
}

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

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def decode_tileset(ts):
    """Return a PIL Image from an embedded base64 tileset entry."""
    data = ts["data"]
    # strip "data:image/png;base64," prefix
    b64 = data.split(",", 1)[1]
    raw = base64.b64decode(b64)
    return Image.open(io.BytesIO(raw)).convert("RGB")

def render(level):
    tile_px  = level["tileSize"]          # 16
    map_w    = level["width"]             # 20
    map_h    = level["height"]            # 18
    canvas_w = map_w * tile_px            # 320
    canvas_h = map_h * tile_px            # 288

    # Build tileset map: numeric id -> PIL image
    # The JSON stores tilesets with string ids, but layer data references
    # numeric ids (ms timestamps).  We discover the mapping by the order in
    # which numeric ids first appear in the layer data — matching them to the
    # tilesets array in order of first encounter.
    tilesets_raw = level["tilesets"]
    ts_images = [decode_tileset(ts) for ts in tilesets_raw]

    # Collect unique numeric tileset ids and their max tile coordinates
    layer = next(l for l in level["layers"] if l["name"] == "Background")
    id_bounds = {}
    for row in layer["data"]:
        for cell in row:
            if isinstance(cell, dict):
                tid = cell["tilesetId"]
                if tid not in id_bounds:
                    id_bounds[tid] = [0, 0]
                id_bounds[tid][0] = max(id_bounds[tid][0], cell["tileX"])
                id_bounds[tid][1] = max(id_bounds[tid][1], cell["tileY"])

    # Known-correct mappings confirmed by user inspection.
    # Key: numeric tilesetId, Value: tileset name as it appears in JSON.
    KNOWN = {
        1784572843253: "kanto8x8",       # top brick-wall rows
        1784573174375: "champions_room", # bikes (tiles 12-15, rows 0-1)
        1784573251738: "champions_room", # dotted courtyard floor
        1784573400361: "forest",         # tree
        1784573550212: "Default Tileset", # courtyard corner/horizontal outline (tiles 6,2 / 7,2)
        1784573750916: "Default Tileset", # wall, stairs, yard outline
    }

    # Build name->index lookup
    name_to_idx = {ts["name"]: i for i, ts in enumerate(tilesets_raw)}

    assigned = set()
    id_to_img = {}
    print("  Tileset id mapping:")

    # Apply known mappings first
    for tid, name in KNOWN.items():
        if tid not in id_bounds:
            continue
        i = name_to_idx[name]
        assigned.add(i)
        id_to_img[tid] = ts_images[i]
        ts = tilesets_raw[i]
        print("    id %d -> [%d] %s (%dx%d)  [confirmed]" % (
            tid, i, ts["name"], ts["cols"], ts["rows"]))

    # Greedy for the rest: sorted timestamp -> first unassigned valid tileset
    for tid in sorted(id_bounds):
        if tid in id_to_img:
            continue
        mx, my = id_bounds[tid]
        for i, ts in enumerate(tilesets_raw):
            if i not in assigned and ts["cols"] > mx and ts["rows"] > my:
                assigned.add(i)
                id_to_img[tid] = ts_images[i]
                print("    id %d -> [%d] %s (%dx%d)  [greedy]" % (
                    tid, i, ts["name"], ts["cols"], ts["rows"]))
                break
        else:
            raise ValueError("No valid tileset for id %d (needs >%d cols, >%d rows)" % (
                tid, mx, my))

    # Build 160x144 directly — each tile = 8x8 output pixels
    OUT_TS = 8
    canvas = Image.new("RGB", (map_w * OUT_TS, map_h * OUT_TS), (255, 255, 255))

    # Precompute actual pixel size per tileset image
    id_to_ts_info = {}
    for tid, img in id_to_img.items():
        ts_idx = list(id_to_img.values()).index(img)
        # actual tile pixel size = image width / number of cols
        # find which tileset this image belongs to
        pass

    # Build id -> (image, actual_tile_px) for rendering — derived from id_to_img
    id_map = {}
    for tid, img in id_to_img.items():
        for i, ts in enumerate(tilesets_raw):
            if ts_images[i] is img:
                actual_px = img.width // ts["cols"]
                id_map[tid] = (img, actual_px)
                break

    for ry, row in enumerate(layer["data"]):
        for rx, cell in enumerate(row):
            if not isinstance(cell, dict):
                continue
            img, actual_px = id_map[cell["tilesetId"]]
            tx, ty = cell["tileX"] * actual_px, cell["tileY"] * actual_px
            tile_img = img.crop((tx, ty, tx + actual_px, ty + actual_px))
            if actual_px != OUT_TS:
                tile_img = tile_img.resize((OUT_TS, OUT_TS), Image.LANCZOS)
            canvas.paste(tile_img, (rx * OUT_TS, ry * OUT_TS))

    return canvas

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    json_path  = sys.argv[1]
    scene_name = sys.argv[2]

    level = load_json(json_path)
    print(f"Loaded {json_path}  ({level['width']}x{level['height']} tiles, tileSize={level['tileSize']})")

    canvas = render(level)

    # Place sprites before palette quantization
    for entry in SCENE_SPRITES.get(scene_name, []):
        place_sprite(canvas, *entry)

    canvas = to_gbpal(canvas)

    out_png = os.path.join(ROOT, "gfx", "scenes", f"{scene_name}.png")
    canvas.save(out_png)
    print(f"Saved {out_png}")

    c_out   = os.path.join(ROOT, "src", "bg", f"scene_{scene_name}.c")
    png2asset = os.path.join(TOOLS, "png2asset.exe")
    cmd = [
        png2asset, out_png,
        "-map", "-use_map_attributes",
        "-bpp", "2",
        "-max_palettes", "1",
        "-tile_origin", "104",
        "-o", c_out,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        sys.exit(1)

    # Inject #pragma bank 2
    with open(c_out) as f:
        content = f.read()
    content = content.replace("\nBANKREF(", "\n#pragma bank 2\nBANKREF(", 1)
    with open(c_out, "w") as f:
        f.write(content)

    m = re.search(r'const uint8_t \w+\[(\d+)\]', content)
    n = int(m.group(1)) // 16 if m else '?'
    print(f"  -> {c_out}  ({n} tiles)")

if __name__ == "__main__":
    main()
