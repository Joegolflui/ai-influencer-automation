#!/usr/bin/env python3
"""Crop 4 characters from reference image."""
from PIL import Image
from pathlib import Path

ROOT = Path("~/csd_girl_group").expanduser()
img = Image.open(ROOT / "references/drug_girl_group_reference.jpg")
w, h = img.size
print(f"Image size: {w}x{h}")

# 4 performers roughly equal width, left to right
chars = [
    ("char1_iceblue", 0, w//4),
    ("char2_purple", w//4, 2*w//4),
    ("char3_green", 2*w//4, 3*w//4),
    ("char4_pink", 3*w//4, w),
]

for name, x1, x2 in chars:
    crop = img.crop((x1, 0, x2, h))
    out = ROOT / f"references/{name}.jpg"
    crop.save(out, quality=95)
    print(f"Saved: {out} ({crop.size})")
