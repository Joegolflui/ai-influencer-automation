#!/usr/bin/env python3
"""
CSD AI Girl Group - LEICA CINEMATIC STYLE v4
Ultra-realistic skin texture, Leica M10, cinematic natural lighting, 4:5 IG ratio
Lens rotation per post group.
"""
import os, base64, requests
from pathlib import Path
import time

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL = "gemini-3.1-flash-image-preview"
ROOT = Path.home() / "csd_girl_group"
REF = ROOT / "references_final"
OUT = ROOT / "output/final_v4_leica"
OUT.mkdir(parents=True, exist_ok=True)

# Lens rotation: 5 poses per character, assign lenses in rotating pattern
# Post 1 (poses 0-3): 90mm, 50mm, 35mm, 28mm
# Post 2 (poses 0-3): 35mm, 90mm, 50mm, 28mm
# Post 3 (poses 0-3): 28mm, 90mm, 35mm, 50mm
# For 5 poses, pose 4 gets 50mm as default
LENS_ROTATION = {
    "binger":  ["90mm", "50mm", "35mm", "28mm", "50mm"],
    "caocao":  ["35mm", "90mm", "50mm", "28mm", "35mm"],
    "xiaoyou": ["28mm", "90mm", "35mm", "50mm", "28mm"],
    "kele":    ["90mm", "35mm", "50mm", "28mm", "90mm"],
}

LENS_DETAILS = {
    "28mm": "Leica Summicron-M 28mm f/2 ASPH, wide-angle environmental portrait, expansive background context, slight edge distortion characteristic of 28mm",
    "35mm": "Leica Summilux-M 35mm f/1.4 ASPH, classic reportage focal length, natural perspective, intimate environmental portrait",
    "50mm": "Leica Summilux-M 50mm f/1.4 ASPH, standard focal length, natural human perspective, versatile portrait",
    "90mm": "Leica APO-Summicron-M 90mm f/2 ASPH, telephoto portrait lens, compressed background, creamy bokeh, tight framing on subject"
}

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

CHARS = {
    "binger": {
        "refs": [REF/"binger_01.jpg", REF/"binger_02.jpg"],
        "frames": sorted((ROOT/"output/binger/frames").glob("binger_ref_*.jpg")),
        "desc": "Silver-blue wavy hair with jeweled headband. Icy blue sequined dress with deep V-neck, dramatic puff sleeves. Youthful face, large eyes, beauty mark, playful smile."
    },
    "caocao": {
        "refs": [REF/"caocao_01.jpg", REF/"caocao_02.jpg"],
        "frames": sorted((ROOT/"output/caocao/frames").glob("caocao_ref_*.jpg")),
        "desc": "Long wavy auburn-brown hair with silver branch accessory. Green gown with leaf embroidery, dramatic organza ruffled sleeves. Gentle warm smile."
    },
    "xiaoyou": {
        "refs": [REF/"xiaoyou_01.jpg"],
        "frames": sorted((ROOT/"output/xiaoyou/frames").glob("xiaoyou_ref_*.jpg")),
        "desc": "Dark hair with purple undertones. Purple-violet-blue gradient gown with asymmetrical sheer strap, crystal embellishments. Bold red lipstick, confident pose."
    },
    "kele": {
        "refs": [REF/"kele_01.jpg", REF/"kele_02.jpg", REF/"kele_03.jpg"],
        "frames": sorted((ROOT/"output/kele/frames").glob("kele_ref_*.jpg")),
        "desc": "Black hair in two high braided pigtails with red beads. Metallic pink-silver dress with 3D star emblem, crystalline shoulder pads. Energetic smile."
    }
}

def build_prompt(char_desc, lens_mm):
    lens_info = LENS_DETAILS[lens_mm]
    return f"""Leica M10 digital rangefinder camera. {lens_info}. Shot on Leica M10.

CHARACTER: {char_desc}

PHOTOGRAPHY STYLE:
- Cinematic natural lighting, no plastic look, no artificial beauty filters
- Soft focus, shallow depth of field, creamy bokeh circles in background
- Natural light, candid抓拍感, Japanese style model photography aesthetic
- Film-like color grading with subtle warm-cool contrast
- Slight lens flare and organic light falloff at edges

SKIN TEXTURE (CRITICAL):
- Ultra-realistic high-fidelity natural skin texture
- Visible fine pores, natural fine lines, subtle skin grain
- Unretouched, healthy and translucent skin tone
- Realistic subsurface scattering on cheeks and nose
- Subtle oil sheen on T-zone (forehead, nose bridge)
- NO over-smoothing, NO plastic feel, NO fake whitening or filter effects
- NO oversaturated fake gloss
- Skin looks like real human skin, not AI-smoothed

COMPOSITION:
- 4:5 vertical portrait ratio (Instagram post format)
- High resolution, sharp focus on eyes with gentle falloff
- Professional fashion editorial quality
- Cinematic color science, muted highlights, rich shadows

NO text, NO logos, NO watermarks."""

def gen(char_id, idx):
    char = CHARS[char_id]
    frame = char["frames"][idx]
    lens_mm = LENS_ROTATION[char_id][idx]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    
    parts = []
    for ref in char["refs"]:
        if ref.exists():
            parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(ref)}})
    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(frame)}})
    parts.append({"text": build_prompt(char["desc"], lens_mm)})
    
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["Text", "Image"], "temperature": 0.2}
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=120)
        data = resp.json()
        if resp.status_code == 200:
            for p in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "inlineData" in p:
                    img = base64.b64decode(p["inlineData"]["data"])
                    out = OUT / f"{char_id}_leica_{lens_mm}_{idx:02d}.png"
                    out.write_bytes(img)
                    return f"OK {lens_mm} ({len(img)} bytes)"
            return "No image"
        return f"HTTP {resp.status_code}"
    except Exception as e:
        return f"ERR: {e}"

for char_id in ["binger", "caocao", "xiaoyou", "kele"]:
    print(f"\n{'='*60}")
    print(f"LEICA STYLE: {char_id.upper()}")
    print(f"{'='*60}")
    for idx in range(5):
        out_file = OUT / f"{char_id}_leica_{LENS_ROTATION[char_id][idx]}_{idx:02d}.png"
        if out_file.exists():
            print(f"  [{idx+1}/5] {LENS_ROTATION[char_id][idx]} SKIP (exists)")
            continue
        print(f"  [{idx+1}/5] {LENS_ROTATION[char_id][idx]} ... ", end="", flush=True)
        result = gen(char_id, idx)
        print(result)
        time.sleep(2)

print("\n\nDone! Final v4 Leica cinematic style complete.")
