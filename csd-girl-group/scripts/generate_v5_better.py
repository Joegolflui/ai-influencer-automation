#!/usr/bin/env python3
"""
CSD AI Girl Group - v5: MORE LIKE VIDEO + BETTER BODY
Ultra-realistic, face must match video references exactly, enhanced figure.
"""
import os, base64, requests
from pathlib import Path
import time

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL = "gemini-3.1-flash-image-preview"
ROOT = Path.home() / "csd_girl_group"
REF = ROOT / "references_final"
OUT = ROOT / "output/final_v5_better"
OUT.mkdir(parents=True, exist_ok=True)

LENS_ROTATION = {
    "binger":  ["90mm", "50mm", "35mm", "28mm", "50mm"],
    "caocao":  ["35mm", "90mm", "50mm", "28mm", "35mm"],
    "xiaoyou": ["28mm", "90mm", "35mm", "50mm", "28mm"],
    "kele":    ["90mm", "35mm", "50mm", "28mm", "90mm"],
}

LENS_DETAILS = {
    "28mm": "Leica Summicron-M 28mm f/2 ASPH, wide-angle environmental portrait",
    "35mm": "Leica Summilux-M 35mm f/1.4 ASPH, natural perspective portrait",
    "50mm": "Leica Summilux-M 50mm f/1.4 ASPH, standard natural portrait",
    "90mm": "Leica APO-Summicron-M 90mm f/2 ASPH, telephoto portrait, creamy bokeh"
}

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

CHARS = {
    "binger": {
        "refs": [REF/"binger_01.jpg", REF/"binger_02.jpg"],
        "frames": sorted((ROOT/"output/binger/frames").glob("binger_ref_*.jpg")),
        "face": "Round cute face, large sparkling double-lidded eyes with visible eyelashes, small delicate nose, natural pink lips in sweet open-mouth smile, fair porcelain skin with beauty mark on left cheek. EXACT face from reference images.",
        "hair": "Shoulder-length wavy silver-blue hair with jeweled crystal headband, voluminous waves framing face, sparkly glitter effect throughout hair.",
        "outfit": "Icy blue sequined mini dress with deep plunging V-neckline, dramatic oversized structured puff sleeves with silver beading and geometric mirrored appliqués, fitted bodice, short skirt above knee.",
        "body": "Enhanced figure: slender waist, fuller bust, elegant hourglass silhouette, long shapely legs. Better proportions than video reference."
    },
    "caocao": {
        "refs": [REF/"caocao_01.jpg", REF/"caocao_02.jpg"],
        "frames": sorted((ROOT/"output/caocao/frames").glob("caocao_ref_*.jpg")),
        "face": "Oval elegant face, gentle warm eyes with subtle smile, small refined nose, natural pink lips slightly parted, healthy wheat-toned skin. EXACT face from reference images.",
        "hair": "Long flowing wavy auburn-brown hair past shoulders, natural breezy waves, delicate silver branch/crystal hair accessory on left temple.",
        "outfit": "Exquisite green gown with sheer illusion bodice, intricate leaf/branch embroidery in emerald and metallic silver, dramatic oversized multi-layered organza ruffled sleeves, voluminous tulle skirt with 3D leaf appliqués.",
        "body": "Enhanced figure: slender elegant frame, graceful long neck, fuller bust, slim waist, elegant proportions. More beautiful than video reference."
    },
    "xiaoyou": {
        "refs": [REF/"xiaoyou_01.jpg", REF/"xiaoyou_02.jpg"],
        "frames": sorted((ROOT/"output/xiaoyou/frames").glob("xiaoyou_ref_*.jpg")),
        "face": "Oval refined face, long slightly upturned mysterious eyes with smoky subtle makeup, small delicate nose, vivid bold red lips in confident smile, fair skin. EXACT face from reference images.",
        "hair": "Shoulder-length wavy dark hair with prominent vivid purple and magenta undertones at ends and underlayers, modern chic bob with waves.",
        "outfit": "Deep purple-indigo-lavender gradient one-shoulder evening gown with sparkly crystalline sequined embellishments on neckline and strap, sheer asymmetric strap, fitted silhouette with crystal decorations.",
        "body": "Enhanced figure: tall elegant stature, slender waist, fuller bust, long shapely legs, confident posture. More stunning than video reference."
    },
    "kele": {
        "refs": [REF/"kele_01.jpg", REF/"kele_02.jpg", REF/"kele_03.jpg"],
        "frames": sorted((ROOT/"output/kele/frames").glob("kele_ref_*.jpg")),
        "face": "Youthful energetic face, large bright expressive eyes, small cute nose, wide dazzling smile with perfect teeth, healthy glowing skin. EXACT face from reference images.",
        "hair": "Black hair in two high braided pigtails with red beads woven throughout length, high placement on head, curls at ends, bangs framing face.",
        "outfit": "Futuristic metallic pink-silver structured dress with deep V-neck, prominent 3D star emblem at chest center, geometric crystalline shoulder pads with translucent iridescent material and red star designs, structured bell skirt with red geometric inserts.",
        "body": "Enhanced figure: athletic-toned build, fuller bust, slim waist, shapely hips, energetic confident posture. More attractive than video reference."
    }
}

def build_prompt(char):
    return f"""CRITICAL: The face MUST be the EXACT SAME PERSON from the character reference images. Match every facial feature, hair color, and outfit detail perfectly.

CHARACTER DESCRIPTION:
- Face: {char['face']}
- Hair: {char['hair']}
- Outfit: {char['outfit']}
- Body: {char['body']}

POSE: Match the pose reference frame exactly for angle, composition, and body position.

PHOTOGRAPHY:
- Leica M10, cinematic natural lighting, soft focus, shallow depth of field
- 4:5 vertical Instagram ratio, high resolution
- Ultra-realistic natural skin texture with visible pores and fine lines
- No plastic look, no over-smoothing, no fake filters
- Professional fashion editorial quality

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
    
    prompt = build_prompt(char)
    prompt += f"\n\nLENS: {LENS_DETAILS[lens_mm]}. Shot on Leica M10."
    parts.append({"text": prompt})
    
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["Text", "Image"], "temperature": 0.15}
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=120)
        data = resp.json()
        if resp.status_code == 200:
            for p in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "inlineData" in p:
                    img = base64.b64decode(p["inlineData"]["data"])
                    out = OUT / f"{char_id}_v5_{lens_mm}_{idx:02d}.png"
                    out.write_bytes(img)
                    return f"OK {lens_mm} ({len(img)} bytes)"
            return "No image"
        return f"HTTP {resp.status_code}"
    except Exception as e:
        return f"ERR: {e}"

for char_id in ["binger", "caocao", "xiaoyou", "kele"]:
    print(f"\n{'='*60}")
    print(f"v5 BETTER: {char_id.upper()}")
    print(f"{'='*60}")
    for idx in range(5):
        lens = LENS_ROTATION[char_id][idx]
        out_file = OUT / f"{char_id}_v5_{lens}_{idx:02d}.png"
        if out_file.exists():
            print(f"  [{idx+1}/5] {lens} SKIP (exists)")
            continue
        print(f"  [{idx+1}/5] {lens} ... ", end="", flush=True)
        result = gen(char_id, idx)
        print(result)
        time.sleep(2)

print("\n\nv5 complete!")
