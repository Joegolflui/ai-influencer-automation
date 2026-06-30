#!/usr/bin/env python3
"""
CSD AI Girl Group - FINAL v3 Generation
Uses MULTIPLE definitive character references + video frame pose references
for maximum consistency and likeness.
"""
import os, base64, requests, json
from pathlib import Path

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL = "gemini-3.1-flash-image-preview"
ROOT = Path.home() / "csd_girl_group"
REF_DIR = ROOT / "references_final"
FRAME_DIR = ROOT / "output"
OUT_DIR = ROOT / "output/final_v3"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Character definitions with their references
CHARS = {
    "binger": {
        "name": "冰兒",
        "refs": ["binger_01.jpg", "binger_02.jpg"],
        "desc": "Silver-blue wavy shoulder-length hair with jeweled headband. Icy blue sequined dress with deep V-neck, dramatic oversized structured puff sleeves with silver beading, geometric mirrored appliqués. Youthful round face, large eyes, beauty mark on left cheek, surprised/playful open-mouth smile."
    },
    "caocao": {
        "name": "草草", 
        "refs": ["caocao_01.jpg", "caocao_02.jpg"],
        "desc": "Long wavy auburn-brown hair with delicate silver branch/crystal hair accessory. Elaborate green gown with sheer illusion bodice, intricate leaf/branch embroidery in emerald and silver, dramatic oversized multi-layered organza ruffled sleeves, voluminous tulle skirt with 3D leaf appliqués. Gentle warm smile."
    },
    "xiaoyou": {
        "name": "小憂",
        "refs": ["xiaoyou_01.jpg"],
        "desc": "Shoulder-length dark hair with prominent purple undertones and highlights. Deep purple-violet-blue gradient evening gown with asymmetrical sheer strap, intricate crystal/rhinestone swirl embellishments on bodice, corseted structured bodice with sheer mesh panels, layered purple-blue tulle skirt. Bold red lipstick, confident smile, left hand on hip."
    },
    "kele": {
        "name": "可樂",
        "refs": ["kele_01.jpg", "kele_02.jpg", "kele_03.jpg"],
        "desc": "Black hair in two high braided pigtails with red beads woven throughout. Futuristic metallic pink-silver dress with deep V-neck, prominent 3D star emblem at chest center, geometric crystalline shoulder pads with translucent iridescent material and red star designs, structured bell skirt with red geometric inserts. Bright energetic smile, holding microphone."
    }
}

def generate(char_id, pose_idx, frame_path):
    char = CHARS[char_id]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    
    # Build parts: all character refs + pose frame + prompt
    parts = []
    
    # Add character appearance references
    for ref_name in char["refs"]:
        ref_path = REF_DIR / ref_name
        if ref_path.exists():
            parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(ref_path)}})
    
    # Add pose reference frame
    parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64(frame_path)}})
    
    # Strong prompt
    prompt = f"""You have {len(char['refs'])} character reference images showing the EXACT appearance of {char['name']}, and 1 pose reference image.

CHARACTER DETAILS:
{char['desc']}

CRITICAL INSTRUCTIONS:
1. The face in the output MUST match the character references EXACTLY - same person, same facial features, same hair
2. The outfit MUST match the character references EXACTLY - same dress, same colors, same details
3. The pose, angle, and composition MUST match the pose reference image EXACTLY
4. Upgrade to 4K photorealistic quality, professional stage photography
5. Keep the stage lighting and background atmosphere from the pose reference
6. 3:4 vertical ratio portrait
7. NO text, NO logos, NO watermarks

Generate the character {char['name']} in the exact pose from the pose reference, with her exact appearance from the character references."""
    
    parts.append({"text": prompt})
    
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["Text", "Image"], "temperature": 0.15}
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=120)
        data = resp.json()
        if resp.status_code == 200:
            parts_out = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            for p in parts_out:
                if "inlineData" in p:
                    img = base64.b64decode(p["inlineData"]["data"])
                    out = OUT_DIR / f"{char_id}_pose_{pose_idx:02d}.png"
                    out.write_bytes(img)
                    return f"{out.name} ({len(img)} bytes)"
            return "No image"
        return f"ERROR {resp.status_code}"
    except Exception as e:
        return f"EXCEPTION: {e}"

def main():
    # Generate 5 poses per character
    for char_id, char_data in CHARS.items():
        print(f"\n{'='*50}")
        print(f"GENERATING {char_id.upper()} - {char_data['name']}")
        print(f"{'='*50}")
        
        # Get video frames for this character
        frames = sorted((FRAME_DIR / char_id / "frames").glob(f"{char_id}_ref_*.jpg"))
        if len(frames) < 5:
            print(f"  WARNING: Only {len(frames)} frames found, need 5")
            frames = frames + [frames[-1]] * (5 - len(frames)) if frames else []
        
        for idx, frame in enumerate(frames[:5]):
            print(f"  [{idx+1}/5] {frame.name} -> ", end="", flush=True)
            result = generate(char_id, idx, frame)
            print(result)

if __name__ == "__main__":
    main()
