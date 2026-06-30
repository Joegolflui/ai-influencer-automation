#!/usr/bin/env python3
"""
CSD AI Girl Group - v8 EXACT LIKENESS
Uses user's uploaded frames as definitive character references.
Stronger emphasis on exact face/hair/costume matching.
"""
import os, base64, requests
from pathlib import Path
import time

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL = "gemini-3.1-flash-image-preview"
ROOT = Path.home() / "csd_girl_group"
REF = ROOT / "references_final"
OUT = ROOT / "output/final_v8_exact"
OUT.mkdir(parents=True, exist_ok=True)

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

CHARACTERS = {
    "binger": {
        "name": "冰兒",
        "desc": "Silver-blue wavy shoulder-length hair, sparkling jeweled headband woven into hair, crystal chandelier earrings, small beauty mark on left cheek. Icy pale-blue sequined dress with dramatic structured geometric crystalline shoulders, deep V-neck with black-and-white triangular bodice pattern, sheer organza ruffled short sleeves. Youthful expressive face, large bright eyes, playful open smile. Fair porcelain skin.",
        "lenses": ["90mm", "50mm", "35mm", "28mm", "50mm"],
    },
    "caocao": {
        "name": "草草",
        "desc": "Long wavy light auburn-brown hair past shoulders with small delicate braids and pearl hair accessories, dangling earrings. Elaborate green gown with sheer nude illusion mesh bodice, prominent cannabis leaf embroidery in metallic green and silver beading tracing stems and veins, dramatic oversized layered organza ruffled off-shoulder sleeves in mint-to-emerald ombre. Warm gentle smile, cheerful expression. Fair skin, elegant features.",
        "lenses": ["35mm", "90mm", "50mm", "28mm", "35mm"],
    },
    "xiaoyou": {
        "name": "小悠",
        "desc": "Shoulder-length dark hair with prominent vivid purple and violet dyed undertones at ends, soft waves with side part. Asymmetrical one-shoulder gown in periwinkle blue, lavender, deep purple with sheer mesh illusion panels on shoulder and chest. Intricate crystal, rhinestone and sequin embellishments in swirling organic patterns on bodice. Small beauty mark on left cheek. Gentle confident smile, hand on hip or playful pointing gesture. Fair skin, defined eyes, arched eyebrows.",
        "lenses": ["28mm", "90mm", "35mm", "50mm", "28mm"],
    },
    "kele": {
        "name": "可樂",
        "desc": "Black hair in two high braided pigtails with small red spherical beads woven throughout the braids. Elaborate theatrical performance costume: metallic crimson-red and rose-pink bodice with deep plunging V-neckline, sheer transparent mesh panels, rhinestone and crystal studded seams. Structured geometric translucent crystalline shoulder armor/epaulets with red accents. Confident bright energetic smile, direct eye contact, dramatic stage makeup with defined eyes. Fair skin.",
        "lenses": ["90mm", "35mm", "50mm", "28mm", "90mm"],
    },
}

LENS = {
    "28mm": "Leica Summicron-M 28mm f/2 ASPH, wide environmental portrait, expansive background context, dramatic perspective",
    "35mm": "Leica Summilux-M 35mm f/1.4 ASPH, classic reportage perspective, natural field of view, photojournalistic feel",
    "50mm": "Leica Summilux-M 50mm f/1.4 ASPH, standard portrait perspective, versatile natural view, balanced composition",
    "90mm": "Leica APO-Summicron-M 90mm f/2 ASPH, telephoto portrait, compressed background, creamy bokeh, intimate framing",
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

for char_key, info in CHARACTERS.items():
    print(f"\n{'='*60}")
    print(f"v8 EXACT: {info['name']} - {char_key.upper()}")
    print(f"{'='*60}")

    # Character references from references_final/{char}/
    char_refs = sorted((REF / char_key).glob("*.jpg"))
    if not char_refs:
        print(f"  SKIP: no character refs found in {REF/char_key}")
        continue

    # Pose references from output/{char}/frames/
    pose_dir = ROOT / "output" / char_key / "frames"
    pose_files = sorted(pose_dir.glob(f"{char_key}_ref_*.jpg"))
    if not pose_files:
        print(f"  SKIP: no pose refs found in {pose_dir}")
        continue

    for idx, (pose_path, lens) in enumerate(zip(pose_files, info["lenses"])):
        out_name = f"{char_key}_v8_{lens}_{idx:02d}.png"
        out_path = OUT / out_name

        if out_path.exists():
            print(f"  [{idx+1}/5] {lens} ... SKIP (exists)")
            continue

        # Build parts: ALL character refs + pose ref
        parts = []
        for fp in char_refs:
            parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(fp)}})
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(pose_path)}})

        prompt = f"""ABSOLUTE MANDATORY: The face structure, hair color, hair style, facial features, and costume MUST be IDENTICAL to the character reference images. Copy the face exactly — same eyes, nose, lips, jawline, expression. Copy the hair exactly — same color, length, waves, and accessories. Copy the costume exactly — same dress design, colors, embellishments, and silhouette. Do NOT alter, idealize, or redesign anything.

Character: {info['name']}
Detailed appearance: {info['desc']}

POSE REFERENCE: The last image shows the exact pose, angle, gesture, and body positioning to replicate. Match this pose precisely.

LENS: {LENS[lens]}

STYLE: Shot on Leica M10 with {lens} lens. Cinematic natural lighting, soft focus, shallow depth of field, natural light, candid Japanese fashion photography feel. Ultra-realistic high-fidelity natural skin texture with visible fine pores, natural fine lines, subtle skin grain. Unretouched healthy translucent skin tone, realistic subsurface scattering, subtle oil sheen on T-zone. Photorealistic, absolutely NO plastic look.

NEGATIVE: No over-smoothing, no plastic appearance, no fake whitening or filter effects, no oversaturated fake gloss. NO anime, NO illustration, NO 3D render look. Must look like a real photograph.

ASPECT RATIO: 4:5 portrait orientation for Instagram.
NO text. NO logos."""

        parts.append({"text": prompt})
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["Text", "Image"],
                "temperature": 0.05,
            }
        }

        try:
            resp = requests.post(url, json=payload, timeout=120)
            data = resp.json()
            if resp.status_code == 200:
                for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                    if "inlineData" in part:
                        img = base64.b64decode(part["inlineData"]["data"])
                        out_path.write_bytes(img)
                        print(f"  [{idx+1}/5] {lens} ... OK ({len(img)} bytes)")
                        break
                else:
                    print(f"  [{idx+1}/5] {lens} ... ERR: No image in response")
            else:
                err = data.get("error", {}).get("message", str(data))[:80]
                print(f"  [{idx+1}/5] {lens} ... ERR: {err}")
        except Exception as e:
            print(f"  [{idx+1}/5] {lens} ... ERR: {e}")

        time.sleep(2)

print("\nv8 EXACT generation complete!")
