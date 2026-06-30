#!/usr/bin/env python3
"""
CSD AI Girl Group - v8b EXACT STYLE MATCH
Uses user's frames as ONLY references. Matches exact art style, face, hair, costume.
No photorealistic/Leica emphasis - matches the digital character aesthetic of refs.
"""
import os, base64, requests
from pathlib import Path
import time

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL = "gemini-3.1-flash-image-preview"
ROOT = Path.home() / "csd_girl_group"
REF = ROOT / "references_final"
OUT = ROOT / "output/final_v8b_exact"
OUT.mkdir(parents=True, exist_ok=True)

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

CHARACTERS = {
    "binger": {
        "name": "冰兒",
        "refs": ["img_989615572e38.jpg","img_0eb712d1fca1.jpg","img_187698447be5.jpg","img_9b26562d8cf2.jpg","img_e48596ab9ae2.jpg"],
        "lenses": ["90mm", "50mm", "35mm", "28mm", "50mm"],
        "poses": [
            "Pointing finger at temple/head, playful smile",
            "Beckoning hand gesture toward viewer, palm up, confident smile",
            "Bright open smile, hand raised near face, energetic stage pose",
            "Hand on hip, other hand pointing up, bright wide smile",
            "Right hand extended forward toward camera, playful presenting gesture",
        ]
    },
    "caocao": {
        "name": "草草",
        "refs": ["img_4709a8a2c934.jpg","img_60a29bec932b.jpg"],
        "lenses": ["35mm", "90mm", "50mm", "28mm", "35mm"],
        "poses": [
            "Gentle warm smile, slight head tilt, relaxed elegant pose",
            "Singing pose, mouth slightly open, emotional expression",
            "Cheerful smile, hand gesture, lively stage presence",
            "Full body wide shot, arms slightly out, showing full green dress",
            "Close-up portrait, warm gentle smile, looking at camera",
        ]
    },
    "xiaoyou": {
        "name": "小悠",
        "refs": ["img_94155177993a.jpg","img_02909a57bafb.jpg","img_ea3e2926be2f.jpg","img_67f465e67793.jpg"],
        "lenses": ["28mm", "90mm", "35mm", "50mm", "28mm"],
        "poses": [
            "Confident smile, hand on hip, direct eye contact",
            "Gentle subtle smile, elegant pose, looking at camera",
            "Bright smile, hand raised near shoulder, playful pointing gesture",
            "Soft gentle expression, head slightly tilted, elegant posture",
            "Full body wide shot, showing full asymmetrical purple dress",
        ]
    },
    "kele": {
        "name": "可樂",
        "refs": ["img_1c19e50dabaf.jpg","img_700635292087.jpg","img_6b2856c491a7.jpg","img_5dd748542834.jpg"],
        "lenses": ["90mm", "35mm", "50mm", "28mm", "90mm"],
        "poses": [
            "Pointing directly at camera with index finger, thumb up, confident smirk",
            "Energetic singing pose, mouth open, expressive stage performance",
            "Bright smile, both hands gesturing, high energy idol pose",
            "Full body wide shot, dynamic stage pose, showing full red costume",
            "Close-up portrait, confident direct gaze, slight playful smile",
        ]
    },
}

LENS = {
    "28mm": "wide environmental shot, showing full body and background context",
    "35mm": "medium shot, natural perspective, subject with some background",
    "50mm": "standard portrait, waist-up framing, balanced composition",
    "90mm": "tight close-up portrait, compressed background, intimate framing",
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

for char_key, info in CHARACTERS.items():
    print(f"\n{'='*60}")
    print(f"v8b EXACT: {info['name']} - {char_key.upper()}")
    print(f"{'='*60}")

    for idx, (lens, pose_desc) in enumerate(zip(info["lenses"], info["poses"])):
        out_name = f"{char_key}_v8b_{lens}_{idx:02d}.png"
        out_path = OUT / out_name

        if out_path.exists():
            print(f"  [{idx+1}/5] {lens} ... SKIP (exists)")
            continue

        # Use ALL user refs for this character
        parts = []
        for rf in info["refs"]:
            fp = REF / char_key / rf
            if fp.exists():
                parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(fp)}})

        prompt = f"""MISSION: Create an image that looks EXACTLY like the character in the reference images. The face, hair color, hair style, facial features, skin texture, and overall visual aesthetic MUST be IDENTICAL to the references.

CRITICAL INSTRUCTIONS:
1. Copy the face EXACTLY — same eye shape, nose, lips, jawline, face proportions, skin tone, makeup style
2. Copy the hair EXACTLY — same color, length, waves, styling, and any accessories
3. Copy the costume EXACTLY — same dress design, colors, embellishments, neckline, sleeves
4. Match the ART STYLE exactly — same lighting quality, smoothness, color grading, and digital aesthetic as the reference images
5. Do NOT make it look like a photograph of a real person. Match the polished digital/AI character look of the references.

POSE: {pose_desc}

FRAMING: {LENS[lens]}

ASPECT RATIO: 4:5 portrait orientation.
NO text. NO logos. NO watermarks."""

        parts.append({"text": prompt})
        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["Text", "Image"],
                "temperature": 0.03,
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

print("\nv8b EXACT generation complete!")
