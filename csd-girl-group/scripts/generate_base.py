#!/usr/bin/env python3
"""
CSD AI Girl Group - Base Reference Portrait Generator
Uses Gemini 2.0 Flash Image Generation to create consistent character references.
"""
import json
import os
import sys
import base64
import requests
from pathlib import Path

# Config
API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL_NAME = "gemini-3.1-flash-image-preview"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
ROOT = Path("~/csd_girl_group").expanduser()
OUTPUT_DIR = ROOT / "references"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_portrait(character, idx):
    """Generate a clean base portrait for a character."""
    name = character["name"]
    app = character["appearance"]
    
    # Build a detailed, consistent prompt
    prompt = f"""A highly detailed, photorealistic portrait photograph of a young Hong Kong Chinese woman named {name}.

EXACT FACE DESCRIPTION (must match in all future images):
- Face shape: {app['face']}
- Hair: {app['hair']}
- Body type: {app['body']}
- Signature expression: {app['signature']}

POSE & COMPOSITION:
- Facing camera directly, shoulders slightly turned
- Neutral, clean studio background in soft {character['bg_color']} tone
- Soft diffused lighting, no harsh shadows
- Shot at eye level, medium close-up (chest up)
- High-end beauty photography style, sharp focus on eyes

RULES:
- EXACT same face must be reproducible across all generations
- No text, no logos, no watermarks
- 4:5 aspect ratio vertical portrait
- Natural skin texture, pores visible, not overly smoothed
"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"],
            "temperature": 0.4,
        }
    }
    
    url = f"{BASE_URL}?key={API_KEY}"
    print(f"[{idx+1}/4] Generating base portrait for {name}...")
    
    try:
        resp = requests.post(url, json=payload, timeout=120)
        data = resp.json()
        
        if resp.status_code != 200:
            print(f"  ERROR HTTP {resp.status_code}: {data}")
            return None
            
        # Extract image from response
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        for part in parts:
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                out_path = OUTPUT_DIR / f"{character['id']}_base_01.png"
                out_path.write_bytes(img_data)
                print(f"  SAVED: {out_path} ({len(img_data)} bytes)")
                return str(out_path)
            elif "text" in part:
                print(f"  TEXT: {part['text'][:200]}")
        
        print(f"  WARNING: No image found in response")
        return None
        
    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return None

def main():
    chars_path = ROOT / "characters" / "characters.json"
    if not chars_path.exists():
        print(f"Characters file not found: {chars_path}")
        sys.exit(1)
    
    with open(chars_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    members = [m for m in data["members"] if m["id"] != "member4"]
    print(f"Generating base portraits for {len(members)} characters...\n")
    
    results = {}
    for idx, char in enumerate(members):
        path = generate_portrait(char, idx)
        results[char["id"]] = path
    
    print("\n=== RESULTS ===")
    for cid, path in results.items():
        status = "OK" if path else "FAILED"
        print(f"  {cid}: {status}")
    
    return results

if __name__ == "__main__":
    main()
