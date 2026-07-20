"""
Convert pokecrystal trainer sprites to GBC 2bpp OBJ tile arrays.
Uses 8x16 sprite mode: each OBJ covers 8x16 pixels (2 stacked tiles).
A 56x56 portrait needs 7x4 = 28 OBJs = 56 tile pairs (56 tiles total).
Source sprites are used at NATIVE 56x56 resolution — no scaling.

GBC 2bpp tile format (16 bytes per 8x8 tile):
  For each of 8 pixel rows, 2 bytes: low-plane, high-plane.
  Pixel palette index = (high_bit << 1) | low_bit.
  Bit 7 of each byte = leftmost pixel.

  For 8x16 OBJ sprites:
    OBJ i uses tile (2*i) for top 8 rows and tile (2*i+1) for bottom 8 rows.
    Tile data must be laid out in OBJ order: [top_i, bot_i, top_i+1, bot_i+1, ...]

OBJ palette index 0 is ALWAYS transparent for sprites.
  idx 0 -> alpha=0 pixels (background around character)
  idx 1 -> light shade (bright skin, highlights)
  idx 2 -> mid shade
  idx 3 -> dark (outlines, shadows)

Output: src/portraits.h, src/portraits.c
"""
from PIL import Image
import numpy as np
import os

ROOT    = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TRAINER = os.path.join(ROOT, "gfx", "pokecrystal-src", "gfx", "trainers")

# Portrait dimensions: native source size
SRC_W = 56   # typical trainer sprite width
SRC_H = 56   # typical trainer sprite height

SPR_COLS = 7    # OBJ columns  (7 * 8 = 56px)
SPR_ROWS = 4    # OBJ rows in 8x16 mode (4 * 16 = 64px; bottom 8px hidden by text box)
N_OBJS   = SPR_COLS * SPR_ROWS   # 28 OBJs total
N_TILES  = N_OBJS * 2             # 56 tiles (top + bottom half per OBJ)

CHARS = [
    ("portrait_michel",   "cooltrainer_m"),
    ("portrait_tobi",     "youngster"),
    ("portrait_friets",   "morty"),
    ("portrait_dad",      "gentleman"),
    ("portrait_teacher",  "teacher"),
    ("portrait_waitress", "beauty"),
    ("portrait_aronian",  "scientist"),
    ("portrait_bramt",    "schoolboy"),
    ("portrait_npc",      "hiker"),
    ("portrait_gerrit",   "sailor"),
    ("portrait_tita",     "camper"),
    ("portrait_divinity", "mysticalman"),
    ("portrait_aerendil", "jasmine"),
]

SPEAKER_MAP = [
    ("MICHEL",   "portrait_michel"),
    ("TOBI",     "portrait_tobi"),
    ("OZORA",    "portrait_tobi"),
    ("FRIETS",   "portrait_friets"),
    ("DAD",      "portrait_dad"),
    ("TEACHER",  "portrait_teacher"),
    ("WAITRESS", "portrait_waitress"),
    ("ARONIAN",  "portrait_aronian"),
    ("BRAMT",    "portrait_bramt"),
    ("BENNY",    "portrait_bramt"),
    ("XOH",      "portrait_michel"),
    ("NPC",      "portrait_npc"),
    ("GERRIT",   "portrait_gerrit"),
    ("TITA",     "portrait_tita"),
    ("DIVINITY", "portrait_divinity"),
    ("AERENDIL", "portrait_aerendil"),
    ("AYARO",    "portrait_bramt"),
]

def pixel_to_idx(r, g, b, a):
    if a < 128:
        return 0   # transparent
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    if   gray > 170: return 1   # light
    elif gray >  85: return 2   # mid
    else:            return 3   # dark

def encode_tile(arr, tile_y, tile_x):
    """Encode one 8x8 region (tile_y, tile_x in pixel coords) to 16 2bpp bytes."""
    out = []
    for row in range(8):
        y = tile_y + row
        lo = hi = 0
        for col in range(8):
            x = tile_x + col
            if y < arr.shape[0] and x < arr.shape[1]:
                px = arr[y, x]
                idx = pixel_to_idx(int(px[0]), int(px[1]), int(px[2]), int(px[3]))
            else:
                idx = 0   # transparent padding
            bit = 7 - col
            lo |= (idx & 1)        << bit
            hi |= ((idx >> 1) & 1) << bit
        out.extend([lo, hi])
    return out

def to_gbc_tiles_8x16(img_rgba):
    """
    Convert RGBA image to GBC 2bpp tiles for 8x16 OBJ sprite mode.
    Output tile order: for each OBJ (row-major), top-half tile then bottom-half tile.
    OBJ i -> tiles[2*i] = top 8 rows, tiles[2*i+1] = bottom 8 rows.
    """
    arr = np.array(img_rgba, dtype=np.uint8)
    out = []
    for obj_row in range(SPR_ROWS):   # 4 rows of 16px
        for obj_col in range(SPR_COLS): # 7 cols of 8px
            px = obj_col * 8
            py = obj_row * 16
            out += encode_tile(arr, py,     px)   # top half
            out += encode_tile(arr, py + 8, px)   # bottom half
    return out   # N_TILES * 16 bytes

def convert_one(c_name, filename):
    src_path = os.path.join(TRAINER, f"{filename}.png")
    img = Image.open(src_path).convert("RGBA")
    # Resize to exactly SRC_W x SRC_H (native; most trainers are already 56x56)
    img = img.resize((SRC_W, SRC_H), Image.NEAREST)
    tile_bytes = to_gbc_tiles_8x16(img)
    assert len(tile_bytes) == N_TILES * 16, f"unexpected tile byte count: {len(tile_bytes)}"
    print(f"  {filename}: {N_TILES} tiles ({len(tile_bytes)} bytes), {SRC_W}x{SRC_H}px native")
    return {"c_name": c_name, "tile_bytes": tile_bytes}

results = [convert_one(*c) for c in CHARS]

# ── portraits.h ───────────────────────────────────────────────────────────────
with open(os.path.join(ROOT, "src", "portraits.h"), "w") as h:
    h.write("#pragma once\n#include <stdint.h>\n\n")
    h.write(f"/* {SPR_COLS}x{SPR_ROWS} OBJ grid (8x16 sprite mode) = {SRC_W}x{SRC_H}px native */\n")
    h.write(f"#define PORTRAIT_SPR_COLS  {SPR_COLS}\n")
    h.write(f"#define PORTRAIT_SPR_ROWS  {SPR_ROWS}\n")
    h.write(f"#define PORTRAIT_N_OBJS    {N_OBJS}\n")
    h.write(f"#define PORTRAIT_TILES     {N_TILES}\n\n")
    h.write("typedef struct {\n")
    h.write(f"    const uint8_t *tiles;  /* {N_TILES}*16 bytes, GBC 2bpp */\n")
    h.write("} portrait_t;\n\n")
    for r in results:
        h.write(f"extern const portrait_t {r['c_name']};\n")
    h.write("\nconst portrait_t *portrait_for_speaker(const char *name);\n")
print("Wrote src/portraits.h")

# ── portraits.c ───────────────────────────────────────────────────────────────
with open(os.path.join(ROOT, "src", "portraits.c"), "w") as c:
    c.write('#include "portraits.h"\n#include <string.h>\n\n')
    for r in results:
        n  = r['c_name']
        bs = r['tile_bytes']
        hex_bytes = ", ".join(f"0x{b:02X}" for b in bs)
        c.write(f"static const uint8_t _{n}_tiles[{N_TILES}*16] = {{\n    {hex_bytes}\n}};\n")
        c.write(f"const portrait_t {n} = {{ _{n}_tiles }};\n\n")

    c.write("const portrait_t *portrait_for_speaker(const char *name) {\n")
    for sp, ptr in SPEAKER_MAP:
        c.write(f'    if (strcmp(name, "{sp}") == 0) return &{ptr};\n')
    c.write("    return 0;\n}\n")
print("Wrote src/portraits.c")
