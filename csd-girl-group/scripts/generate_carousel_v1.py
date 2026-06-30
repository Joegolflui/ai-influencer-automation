#!/usr/bin/env python3
"""
CSD AI Girl Group - Carousel v1
Outdoor editorial settings, exact character faces, Leica M10 cinematic style.
3 posts per character, 4 images each, lens rotation per user spec.
"""
import os, base64, requests
from pathlib import Path
import time

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL = "gemini-3.1-flash-image-preview"
ROOT = Path.home() / "csd_girl_group"
REF = ROOT / "references_final"
OUT = ROOT / "output/carousel_v1"

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

CHARACTERS = {
    "binger": {
        "name": "冰兒",
        "desc": "Silver-blue wavy shoulder-length hair, sparkling jeweled headband, crystal chandelier earrings, small beauty mark on left cheek. Icy pale-blue sequined dress with dramatic structured geometric crystalline shoulders, deep V-neck, sheer organza ruffled short sleeves. Youthful expressive face, large bright eyes, playful smile. Fair porcelain skin.",
        "setting": "Stunning icy glacier landscape with crystal blue ice formations, snow-covered mountains in background, frozen lake reflecting sky. Ethereal winter daylight, soft diffused natural light."
    },
    "caocao": {
        "name": "草草",
        "desc": "Long wavy light auburn-brown hair past shoulders with small delicate braids and pearl hair accessories, dangling earrings. Elaborate green gown with sheer nude illusion mesh bodice, prominent cannabis leaf embroidery in metallic green and silver beading, dramatic oversized layered organza ruffled off-shoulder sleeves in mint-to-emerald ombre. Warm gentle smile. Fair skin, elegant features.",
        "setting": "Endless field of blooming purple lavender under golden hour sunlight, soft-focus mountains and hazy sky in background. Dreamy romantic summer atmosphere, gentle breeze moving hair and dress."
    },
    "xiaoyou": {
        "name": "小悠",
        "desc": "Shoulder-length dark hair with prominent vivid purple and violet dyed undertones at ends, soft waves with side part. Asymmetrical one-shoulder gown in periwinkle blue, lavender, deep purple with sheer mesh illusion panels. Intricate crystal, rhinestone and sequin embellishments in swirling organic patterns on bodice. Small beauty mark on left cheek. Gentle confident smile. Fair skin, defined eyes, arched eyebrows.",
        "setting": "Magical night scene under vast starry sky with aurora borealis in purple and blue, reflecting on calm dark water. Ethereal cosmic atmosphere, soft moonlight mixed with aurora glow."
    },
    "kele": {
        "name": "可樂",
        "desc": "Black hair in two high braided pigtails with small red spherical beads woven throughout the braids. Elaborate theatrical performance costume: metallic crimson-red and rose-pink bodice with deep plunging V-neckline, sheer transparent mesh panels, rhinestone and crystal studded seams. Structured geometric translucent crystalline shoulder armor with red accents. Confident bright energetic smile, direct eye contact. Fair skin.",
        "setting": "Stylish urban rooftop at dusk with city skyline and neon lights in background, warm ambient lighting, modern architecture. Vibrant nightlife atmosphere, soft bokeh from city lights."
    },
}

# 3 posts per character, 4 lenses each
POSTS = [
    ["90mm", "50mm", "35mm", "28mm"],
    ["35mm", "90mm", "50mm", "28mm"],
    ["28mm", "90mm", "35mm", "50mm"],
]

LENS = {
    "28mm": "Leica Summicron-M 28mm f/2 ASPH, wide environmental portrait, expansive background context, dramatic perspective",
    "35mm": "Leica Summilux-M 35mm f/1.4 ASPH, classic reportage perspective, natural field of view, photojournalistic feel",
    "50mm": "Leica Summilux-M 50mm f/1.4 ASPH, standard portrait perspective, versatile natural view, balanced composition",
    "90mm": "Leica APO-Summicron-M 90mm f/2 ASPH, telephoto portrait, compressed background, creamy bokeh, intimate framing",
}

POSES = [
    ["Standing gracefully facing camera with soft smile, one hand touching dress, relaxed elegant posture",
     "Sitting on ground looking at camera, warm smile, natural relaxed pose",
     "Three-quarter turn glancing back over shoulder, bright welcoming smile, hair and dress moving in breeze",
     "Full body wide shot standing tall among scenery, weight shifted onto one leg, one hand lightly touching skirt"],
    ["Close-up portrait with contemplative expression, soft gaze, head slightly tilted",
     "Standing with arms slightly outstretched, joyful expression, looking upward",
     "Walking toward camera with natural stride, hair flowing, confident smile",
     "Full body wide shot, dynamic pose showing full dress in environment"],
    ["Seated pose leaning forward, one hand playfully touching hair, laughing brightly",
     "Over-the-shoulder look back at camera, gentle alluring smile, showing back detail of dress",
     "Standing with one hand on hip, direct confident gaze at camera, strong posture",
     "Full body wide shot, playful pose with movement, dress flowing, energetic expression"],
]

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

for char_key, info in CHARACTERS.items():
    char_out = OUT / char_key
    char_out.mkdir(parents=True, exist_ok=True)

    # Load all face refs
    face_refs = sorted((REF / char_key).glob("*.jpg"))
    if not face_refs:
        print(f"SKIP {char_key}: no refs")
        continue

    for post_idx, lenses in enumerate(POSTS):
        post_out = char_out / f"post_{post_idx+1}"
        post_out.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"{info['name']} - Post {post_idx+1}")
        print(f"{'='*60}")

        for img_idx, (lens, pose) in enumerate(zip(lenses, POSES[post_idx])):
            out_name = f"{char_key}_p{post_idx+1}_{lens}_{img_idx+1}.png"
            out_path = post_out / out_name

            if out_path.exists():
                print(f"  [{img_idx+1}/4] {lens} ... SKIP")
                continue

            parts = []
            for fp in face_refs:
                parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(fp)}})

            prompt = f"""CRITICAL: The face, hair, and overall appearance MUST match the character reference images EXACTLY. Copy the face identically — same eye shape, nose, lips, jawline, face proportions. Copy the hair identically — same color, length, waves, styling, accessories. Copy the costume identically — same dress design, colors, embellishments.

Character: {info['name']}
Appearance: {info['desc']}

SETTING: {info['setting']}

POSE: {pose}

LENS: {LENS[lens]}

STYLE: Shot on Leica M10 with {lens} lens. Cinematic natural lighting, soft focus, shallow depth of field, natural light, candid Japanese fashion photography feel. Ultra-realistic high-fidelity natural skin texture with visible fine pores, natural fine lines, subtle skin grain. Unretouched healthy translucent skin tone, realistic subsurface scattering, subtle oil sheen on T-zone. Cinematic natural lighting, absolutely NO plastic look. Magazine editorial quality.

NEGATIVE: No over-smoothing, no plastic appearance, no fake whitening or filter effects, no oversaturated fake gloss.

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
                            print(f"  [{img_idx+1}/4] {lens} ... OK ({len(img)} bytes)")
                            break
                    else:
                        print(f"  [{img_idx+1}/4] {lens} ... ERR: No image")
                else:
                    err = data.get("error", {}).get("message", str(data))[:60]
                    print(f"  [{img_idx+1}/4] {lens} ... ERR: {err}")
            except Exception as e:
                print(f"  [{img_idx+1}/4] {lens} ... ERR: {e}")

            time.sleep(3)

print("\nCarousel v1 generation complete!")
