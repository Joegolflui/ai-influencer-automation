#!/usr/bin/env python3
"""
CSD AI Girl Group - v7 EXACT LIKENESS
Uses ONLY the user's uploaded frames as definitive character references.
"""
import os, base64, requests
from pathlib import Path

API_KEY = "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE"
MODEL = "gemini-3.1-flash-image-preview"
ROOT = Path.home() / "csd_girl_group"
REF = ROOT / "references_final_v7"
POSES = ROOT / "output"
OUT = ROOT / "output/final_v7_exact"
OUT.mkdir(parents=True, exist_ok=True)

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

CHARACTERS = {
    "binger": {
        "name": "冰兒",
        "frames": ["binger_01.jpg","binger_02.jpg","binger_03.jpg","binger_04.jpg","binger_05.jpg"],
        "desc": "Silver-blue wavy shoulder-length hair, sparkling jeweled headband, crystal chandelier earrings, pale icy-blue sequined dress with dramatic structured geometric shoulders, deep V-neck with black-and-white triangular bodice pattern, sheer organza ruffled sleeves. Expressive open smile, playful surprised gesture with hand near face or beckoning. Fair skin, delicate features, beauty mark on left cheek.",
        "poses": [
            ("binger_frame_01.jpg", "90mm"),
            ("binger_frame_02.jpg", "50mm"),
            ("binger_frame_03.jpg", "35mm"),
            ("binger_frame_04.jpg", "28mm"),
            ("binger_frame_05.jpg", "50mm"),
        ]
    },
    "caocao": {
        "name": "草草",
        "frames": ["caocao_01.jpg","caocao_02.jpg"],
        "desc": "Long wavy light auburn-brown hair past shoulders, small pearl hair accessories, dangling earrings. Elaborate green gown with sheer nude illusion bodice, prominent cannabis leaf embroidery in metallic green and silver beading, dramatic oversized layered organza ruffled off-shoulder sleeves in mint-to-emerald ombre. Warm gentle smile, cheerful expression. Fair skin, elegant features.",
        "poses": [
            ("caocao_ref_00.jpg", "35mm"),
            ("caocao_ref_01.jpg", "90mm"),
            ("caocao_ref_02.jpg", "50mm"),
            ("caocao_ref_03.jpg", "28mm"),
            ("caocao_ref_04.jpg", "35mm"),
        ]
    },
    "xiaoyou": {
        "name": "小悠",
        "frames": ["xiaoyou_01.jpg","xiaoyou_02.jpg","xiaoyou_03.jpg","xiaoyou_04.jpg"],
        "desc": "Shoulder-length dark hair with prominent purple/violet highlights at ends, soft waves. Asymmetrical one-shoulder gown in periwinkle, lavender, deep purple with sheer mesh panels. Intricate crystal, rhinestone and sequin embellishments on bodice. Small beauty mark on left cheek. Gentle subtle smile, confident pose with hand on hip or pointing up. Fair skin, arched eyebrows, defined eyes.",
        "poses": [
            ("xiaoyou_ref_00.jpg", "28mm"),
            ("xiaoyou_ref_01.jpg", "90mm"),
            ("xiaoyou_ref_02.jpg", "35mm"),
            ("xiaoyou_ref_03.jpg", "50mm"),
            ("xiaoyou_ref_04.jpg", "28mm"),
        ]
    },
    "kele": {
        "name": "可樂",
        "frames": ["kele_01.jpg","kele_02.jpg","kele_03.jpg","kele_04.jpg"],
        "desc": "Black hair in two high braided pigtails with small red beads woven throughout. Elaborate theatrical performance costume: metallic crimson/red and rose-pink bodice with deep plunging V-neckline, sheer transparent mesh panels, rhinestone/crystal studded seams. Structured geometric translucent shoulder armor with red star accents. Confident bright smile, energetic pose, thumbs up or singing gesture. Dramatic stage makeup with defined eyes.",
        "poses": [
            ("kele_ref_00.jpg", "90mm"),
            ("kele_ref_01.jpg", "35mm"),
            ("kele_ref_02.jpg", "50mm"),
            ("kele_ref_03.jpg", "28mm"),
            ("kele_ref_04.jpg", "90mm"),
        ]
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
    print(f"v7 EXACT: {info['name']} - {char_key.upper()}")
    print(f"{'='*60}")

    for idx, (pose_file, lens) in enumerate(info["poses"]):
        out_name = f"{char_key}_v7_{lens}_{idx:02d}.png"
        out_path = OUT / out_name

        if out_path.exists():
            print(f"  [{idx+1}/5] {lens} ... SKIP (exists)")
            continue

        # Build references: ALL user frames + pose frame
        parts = []
        for f in info["frames"]:
            fp = REF / f
            if fp.exists():
                parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(fp)}})

        # Add pose reference
        pose_path = POSES / char_key / "frames" / pose_file
        if pose_path.exists():
            parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(pose_path)}})

        prompt = f"""ULTRA CRITICAL: The face, hair, and overall appearance MUST match the character reference images EXACTLY. Do NOT change the face structure, hair color, or facial features.

Character: {info['name']} ({info['desc']})

ENHANCED FIGURE: Beautiful elegant proportions, graceful posture, attractive silhouette.

POSE: Match the pose reference image exactly - same angle, gesture, and body positioning.

LENS: {LENS[lens]}

STYLE: Shot on Leica M10, {lens} lens. Cinematic natural lighting, soft focus, shallow depth of field, natural light, candid Japanese fashion photography feel. Ultra-realistic high-fidelity natural skin texture with visible fine pores, natural fine lines, subtle skin grain. Unretouched healthy translucent skin tone, realistic subsurface scattering, subtle oil sheen on T-zone. Cinematic natural lighting, absolutely NO plastic look.

NEGATIVE: No over-smoothing, no plastic appearance, no fake whitening or filter effects, no oversaturated fake gloss. Photorealistic, not anime or illustration.

ASPECT RATIO: 4:5 portrait orientation for Instagram.
NO text NO logos."""

        parts.append({"text": prompt})
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["Text", "Image"],
                "temperature": 0.08,
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
                        print(f"  [{idx+1}/5] {lens} ... OK {lens} ({len(img)} bytes)")
                        break
                else:
                    print(f"  [{idx+1}/5] {lens} ... ERR: No image in response")
            else:
                err = data.get("error", {}).get("message", str(data))[:60]
                print(f"  [{idx+1}/5] {lens} ... ERR: {err}")
        except Exception as e:
            print(f"  [{idx+1}/5] {lens} ... ERR: {e}")

print("\nv7 EXACT generation complete!")
