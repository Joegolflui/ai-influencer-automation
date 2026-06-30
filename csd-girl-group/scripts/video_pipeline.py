#!/usr/bin/env python3
"""
CSD AI Girl Group - Video Frame Pipeline
1. Extract frames from video
2. Classify each frame by character (face detection + color matching)
3. Image-to-Image generation with Gemini for each character
"""
import json
import os
import base64
import requests
import subprocess
from pathlib import Path
from collections import defaultdict

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAzg8sdqVrDtuINRKTdjqOZ9cIb3tBnDTE")
MODEL_IMG = "gemini-3.1-flash-image-preview"
ROOT = Path("~/csd_girl_group").expanduser()
OUT = ROOT / "output"

def extract_frames(video_path, fps=2):
    """Extract frames from video at specified fps."""
    frames_dir = ROOT / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old frames
    for f in frames_dir.glob("*.jpg"):
        f.unlink()
    
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vf", f"fps={fps},scale=720:-1",
        "-q:v", "2",
        str(frames_dir / "frame_%04d.jpg")
    ]
    print(f"Extracting frames at {fps} fps...")
    subprocess.run(cmd, capture_output=True)
    
    frames = sorted(frames_dir.glob("frame_*.jpg"))
    print(f"Extracted {len(frames)} frames")
    return frames

def classify_frame(frame_path):
    """Classify which character is in the frame using Gemini vision."""
    with open(frame_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"
    prompt = """Look at this image from a video frame. It shows one or more female characters from an AI idol group.

There are 4 characters:
- 冰兒 (Binger): silver-blue hair, light blue dress, cute round face
- 草草 (Caocao): brown/auburn hair, green dress with big sleeves
- 小悠 (Xiaoyou): dark purple hair, purple/blue asymmetric dress
- 可樂 (Kele): black twin braids with red, pink/futuristic dress

Identify which character is the MAIN FOCUS or most prominent in this frame.
Respond with ONLY ONE of: binger, caocao, xiaoyou, kele, or "group" if multiple equally, or "none" if unclear.
Just the single word, nothing else."""

    payload = {
        "contents": [{"parts": [
            {"inlineData": {"mimeType": "image/jpeg", "data": b64}},
            {"text": prompt}
        ]}],
        "generationConfig": {"temperature": 0.1}
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=30)
        data = resp.json()
        text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "none")
        text = text.strip().lower()
        valid = {"binger", "caocao", "xiaoyou", "kele", "group", "none"}
        return text if text in valid else "none"
    except Exception as e:
        print(f"  Classify error: {e}")
        return "none"

def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def generate_i2i(char_id, ref_frame_path, out_idx):
    """Image-to-image generation using frame as reference."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_IMG}:generateContent?key={API_KEY}"
    
    with open(ROOT / "characters/characters_detailed.json", "r") as f:
        chars = json.load(f)
    
    char = next((c for c in chars["members"] if c["id"] == char_id), None)
    if not char:
        return None
    
    b64 = img_to_b64(ref_frame_path)
    
    prompt = f"""Using this video frame as POSE and COMPOSITION reference, recreate the character with HIGHER QUALITY.

Character: {char['name']}
- Face: {char['face']}
- Hair: {char['hair']}
- Outfit: {char['outfit']}
- Expression: {char['expression']}

IMPORTANT:
1. Match the EXACT pose, angle, and composition from the reference frame
2. Replace the person with this specific character's face, hair, and outfit
3. Upgrade to 4K photorealistic quality, professional beauty photography
4. Keep the same background/lighting mood from the reference
5. 3:4 vertical ratio
6. NO text, NO logos
"""
    
    payload = {
        "contents": [{"parts": [
            {"inlineData": {"mimeType": "image/jpeg", "data": b64}},
            {"text": prompt}
        ]}],
        "generationConfig": {"responseModalities": ["Text", "Image"], "temperature": 0.2}
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=120)
        data = resp.json()
        
        if resp.status_code != 200:
            return None
        
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        for part in parts:
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                out_path = OUT / char_id / f"{char_id}_i2i_{out_idx:04d}.png"
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(img_data)
                return str(out_path)
        return None
    except Exception as e:
        print(f"  Gen error: {e}")
        return None

def main(video_path):
    # Step 1: Extract frames
    frames = extract_frames(video_path, fps=2)
    
    # Step 2: Classify frames
    print("\nClassifying frames by character...")
    groups = defaultdict(list)
    for i, frame in enumerate(frames):
        char = classify_frame(frame)
        groups[char].append(frame)
        print(f"  Frame {i+1}/{len(frames)}: {char}")
    
    print(f"\nClassification results:")
    for char, fs in groups.items():
        print(f"  {char}: {len(fs)} frames")
    
    # Step 3: Generate I2I for key characters (skip group/none)
    target_chars = ["binger", "caocao", "xiaoyou", "kele"]
    for char_id in target_chars:
        if char_id not in groups or len(groups[char_id]) == 0:
            continue
        
        print(f"\n=== Generating I2I for {char_id} ===")
        # Pick up to 5 representative frames (evenly spaced)
        frames_for_char = groups[char_id]
        step = max(1, len(frames_for_char) // 5)
        selected = frames_for_char[::step][:5]
        
        for idx, frame in enumerate(selected):
            print(f"  [{idx+1}/{len(selected)}] {frame.name}")
            result = generate_i2i(char_id, frame, idx)
            if result:
                print(f"    -> {result}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python video_pipeline.py <video_path>")
        sys.exit(1)
    main(sys.argv[1])
