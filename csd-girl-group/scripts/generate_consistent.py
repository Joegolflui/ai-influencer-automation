#!/usr/bin/env python3
"""
CSD AI Girl Group - Consistent Character Generator
Uses Gemini 3.1 Flash Image with reference images for consistency.
"""
import json
import os
import base64
import requests
from pathlib import Path

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL = "gemini-3.1-flash-image-preview"
ROOT = Path("~/csd_girl_group").expanduser()
REF_DIR = ROOT / "references"
OUT_DIR = ROOT / "output"

def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def generate_with_ref(char_id, ref_path, prompt, out_name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    
    b64 = img_to_b64(ref_path)
    ext = ref_path.suffix.lower()
    mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    
    payload = {
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": mime, "data": b64}},
                {"text": prompt}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"],
            "temperature": 0.3,
        }
    }
    
    print(f"  Generating {out_name}...")
    try:
        resp = requests.post(url, json=payload, timeout=120)
        data = resp.json()
        
        if resp.status_code != 200:
            print(f"    ERROR HTTP {resp.status_code}: {str(data)[:300]}")
            return None
        
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        for part in parts:
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                out_path = OUT_DIR / char_id / out_name
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(img_data)
                print(f"    SAVED: {out_path} ({len(img_data)} bytes)")
                return str(out_path)
            elif "text" in part:
                print(f"    TEXT: {part['text'][:200]}")
        
        print(f"    WARNING: No image in response")
        return None
    except Exception as e:
        print(f"    EXCEPTION: {e}")
        return None

def main():
    with open(ROOT / "characters/characters.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Map character IDs to reference images (from the cropped refs or new refs)
    # We use the test image we generated earlier as a style reference, 
    # plus text prompts for each character.
    
    prompts = {
        "binger": {
            "portrait": "A highly detailed photorealistic portrait of a young Hong Kong Chinese woman, 20 years old. She has shoulder-length wavy silver-blue hair with a sparkly hair accessory, round face, big bright double-lidded eyes, small nose, delicate mouth, fair translucent skin. She is wearing a light blue sparkly off-shoulder dress with sweetheart neckline, ruffled organza sleeves, layered tulle skirt to knee-length, fine diamond decorations. She points at the camera with one finger, sweet energetic smile. Clean soft light blue studio background. Medium close-up, eye-level shot, beauty photography, 4:5 vertical ratio. EXACT face must be reproducible. No text, no logos.",
            "fullbody": "Full body shot of the same young Hong Kong Chinese woman with silver-blue wavy hair and light blue sparkly dress. Standing confidently with legs slightly apart, one hand on hip, other hand waving. Full dress visible - sweetheart neckline, ruffled sleeves, layered tulle skirt, diamond details. Clean light blue studio background. Eye-level, 4:5 vertical ratio, sharp focus, beauty photography.",
            "pose2": "Same young Hong Kong Chinese woman with silver-blue hair and light blue dress. Sitting casually on a white cube stool, legs crossed, leaning slightly forward, warm smile looking at camera. Clean light blue studio background. Medium shot, 4:5 vertical ratio, natural lighting."
        },
        "caocao": {
            "portrait": "A highly detailed photorealistic portrait of a young Hong Kong Chinese woman, 21 years old. She has long wavy light brown hair with auburn highlights, natural and flowing. Oval face, elongated gentle eyes, slightly upturned eye corners, small nose with subtle bridge, natural pale pink lips, healthy wheat-colored skin. She wears a green dress with cannabis leaf embroidery, large green tulle puff sleeves, layered tulle ruffles, off-shoulder design. Hands gently clasped in front, head slightly tilted, warm gentle smile. Clean soft green studio background. Medium close-up, eye-level, beauty photography, 4:5 vertical ratio. No text.",
            "fullbody": "Full body shot of the same young woman with long light brown wavy hair and green embroidered dress. Standing gracefully, one hand touching her hair, the other relaxed at her side. Full dress visible - cannabis leaf embroidery, large tulle sleeves, layered ruffles. Clean green studio background. Eye-level, 4:5 vertical ratio.",
            "pose2": "Same young woman with light brown hair and green dress. Sitting on a wooden bench in a relaxed pose, legs crossed, looking off to the side with a serene expression. Clean green studio background. Medium shot, 4:5 vertical ratio."
        },
        "kele": {
            "portrait": "A highly detailed photorealistic portrait of a young Hong Kong Chinese woman, 19 years old. She has black hair in two long thick braided pigtails with red hair ties, curls at the ends. Pointed face, big energetic eyes, small nose, wide mouth with full white teeth smile, healthy skin. She wears a shiny red short dress with a cola bottle cap decoration on chest, red leather boots. Fists clenched in front of chest, huge radiant smile, eyes curved like crescent moons, full of energy. Clean soft red studio background. Medium close-up, eye-level, beauty photography, 4:5 vertical ratio. No text.",
            "fullbody": "Full body shot of the same young woman with black braided pigtails and red shiny dress. Standing in a dynamic pose, one leg forward, arms raised in victory pose, huge smile. Full outfit visible - red dress, cola cap decoration, red boots. Clean red studio background. Eye-level, 4:5 vertical ratio.",
            "pose2": "Same young woman with black braided pigtails and red dress. Jumping in mid-air, legs bent, arms spread wide, joyful expression. Clean red studio background. Full body, 4:5 vertical ratio, dynamic action shot."
        },
        "xiaoyou": {
            "portrait": "A highly detailed photorealistic portrait of a young Hong Kong Chinese woman, 20 years old. She has shoulder-length wavy dark purple-black hair with purple highlights and sheen. Oval face, slightly wavy short hair, long slightly upturned eyes, subtle smile, mysterious elf-like temperament. She wears a purple iridescent asymmetrical sleeveless dress with star and galaxy decorations, sequins and crystals, one shoulder exposed. One eye winking, finger lightly touching her cheek, mysterious smile. Clean soft purple studio background. Medium close-up, eye-level, beauty photography, 4:5 vertical ratio. No text.",
            "fullbody": "Full body shot of the same young woman with dark purple wavy hair and purple galaxy dress. Standing elegantly, one hand on hip, other hand raised with fingers slightly spread, mysterious smile. Full dress visible - asymmetrical, star decorations, sequins, one shoulder exposed. Clean purple studio background. Eye-level, 4:5 vertical ratio.",
            "pose2": "Same young woman with dark purple hair and purple dress. Sitting on a transparent acrylic chair, legs crossed, leaning back slightly, looking directly at camera with a confident mysterious expression. Clean purple studio background. Medium shot, 4:5 vertical ratio."
        }
    }
    
    # Reference images from the cropped drug girl group images
    ref_map = {
        "binger": REF_DIR / "char1_iceblue.jpg",
        "caocao": REF_DIR / "char3_green.jpg",
        "kele": REF_DIR / "char4_pink.jpg",
        "xiaoyou": REF_DIR / "char2_purple.jpg",
    }
    
    print(f"Generating consistent portraits for 4 characters x 3 poses each = 12 images...\n")
    
    results = {}
    for char_id, poses in prompts.items():
        ref_path = ref_map.get(char_id)
        if not ref_path or not ref_path.exists():
            print(f"WARNING: No reference for {char_id}, using text-only generation")
            ref_path = None
        
        print(f"\n=== {char_id.upper()} ===")
        char_results = {}
        for pose_name, prompt_text in poses.items():
            out_name = f"{char_id}_{pose_name}.png"
            if ref_path:
                path = generate_with_ref(char_id, ref_path, prompt_text, out_name)
            else:
                # Fallback to text-only
                path = None
            char_results[pose_name] = path
        results[char_id] = char_results
    
    print("\n=== SUMMARY ===")
    for char_id, poses in results.items():
        ok = sum(1 for v in poses.values() if v)
        print(f"  {char_id}: {ok}/3 OK")
    
    return results

if __name__ == "__main__":
    main()
