"""
Convert an image to a GBC-compatible 160x144 title screen PNG and run png2asset.

Usage:
    python tools/convert_title.py <input_image> [scene_name]

    scene_name defaults to "title"

Example:
    python tools/convert_title.py "C:/Users/epe_m/Downloads/Gemini_Generated_Image_yjlubyjlubyjluby.png"
    python tools/convert_title.py "C:/Users/epe_m/Downloads/Gemini_Generated_Image_wbm88kwbm88kwbm8.png" title_brams

Resizes to 160x144, applies a mild blur to flatten dithering into solid tile
regions (reduces unique 8x8 tile count), snaps to the GBC 4-level grayscale
palette, and outputs:
  gfx/scenes/<scene_name>.png
  src/bg/scene_<scene_name>.c  (with #pragma bank 2)
"""

import sys, os, re, subprocess
from PIL import Image, ImageFilter

ROOT    = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS   = os.path.join(ROOT, "tools", "gbdk", "bin")

_LEVELS = [255, 170, 85, 0]

def snap(v):
    return min(_LEVELS, key=lambda l: abs(v - l))

def to_gbpal(img):
    grey = img.convert("L")
    px   = grey.load()
    for y in range(grey.height):
        for x in range(grey.width):
            px[x, y] = snap(px[x, y])
    return grey.convert("RGB")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    src_path   = sys.argv[1]
    scene_name = sys.argv[2] if len(sys.argv) >= 3 else "title"

    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    print(f"Loaded {src_path}  ({w}x{h})")

    # Resize to 160x144
    img = img.resize((160, 144), Image.LANCZOS)
    print(f"Resized to 160x144")

    # Mild blur + median: flatten dithering into solid tile regions.
    # tile_origin=0 gives 256 VRAM slots so we can afford more detail.
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    img = to_gbpal(img)
    img = img.convert("L").filter(ImageFilter.MedianFilter(size=3)).convert("RGB")
    print(f"Blur+median applied")

    # Snap to GBC 4-level palette
    img = to_gbpal(img)

    out_png = os.path.join(ROOT, "gfx", "scenes", f"{scene_name}.png")
    img.save(out_png)
    print(f"Saved {out_png}")

    c_out     = os.path.join(ROOT, "src", "bg", f"scene_{scene_name}.c")
    png2asset = os.path.join(TOOLS, "png2asset.exe")
    cmd = [
        png2asset, out_png,
        "-map", "-use_map_attributes",
        "-bpp", "2",
        "-max_palettes", "1",
        "-tile_origin", "0",
        "-o", c_out,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        sys.exit(1)

    with open(c_out) as f:
        content = f.read()
    content = content.replace("\nBANKREF(", "\n#pragma bank 2\nBANKREF(", 1)
    with open(c_out, "w") as f:
        f.write(content)

    m = re.search(r'const uint8_t \w+\[(\d+)\]', content)
    n = int(m.group(1)) // 16 if m else '?'
    print(f"  -> {c_out}  ({n} tiles)")
    if isinstance(n, int) and n > 256:
        print(f"  WARNING: {n} tiles exceeds 256 VRAM limit — image too complex")

if __name__ == "__main__":
    main()
