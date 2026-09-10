from PIL import Image
import os, glob

W_PX = round(50 / 25.4 * 300)   # 591
H_PX = round(75 / 25.4 * 300)   # 886
DPI  = (300, 300)

src = "labels/FINAL"
dst = "labels/PRINT"
os.makedirs(dst, exist_ok=True)

for path in glob.glob(f"{src}/*"):
    img = Image.open(path)
    img = img.resize((W_PX, H_PX), Image.LANCZOS)
    name = os.path.splitext(os.path.basename(path))[0] + ".png"
    img.save(os.path.join(dst, name), dpi=DPI)
    print(f"{name}: {W_PX}x{H_PX}px @ 300dpi")
