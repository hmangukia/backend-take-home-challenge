from fastapi import APIRouter
from fastapi.responses import FileResponse
from models import FlyerRequest
from typing import List
from PIL import Image, ImageDraw, ImageFont
import os
import uuid
import re

router = APIRouter()

ASSETS_DIR = "assets"
OUTPUT_DIR = "generated"
DEFAULT_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def match_images(prompt: str) -> List[str]:
    prompt_keywords = re.findall(r"\w+", prompt.lower())
    selected_images = []
    for fname in os.listdir(ASSETS_DIR):
        if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        for word in prompt_keywords:
            if word in fname.lower():
                selected_images.append(os.path.join(ASSETS_DIR, fname))
                break
    return selected_images or [
        os.path.join(ASSETS_DIR, f) for f in os.listdir(ASSETS_DIR)[:3]
    ]


def create_flyer(images: List[str], text: str, output_path: str):
    base = Image.new("RGB", (800, 1000), "white")
    y = 20
    for img_path in images[:3]:
        try:
            img = Image.open(img_path).convert("RGB")
            img.thumbnail((760, 250))
            base.paste(img, (20, y))
            y += img.height + 10
        except Exception as e:
            print(f"Failed to add image {img_path}: {e}")

    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(DEFAULT_FONT, size=30)
    draw.text((20, y + 20), text, fill="black", font=font)

    base.save(output_path)


@router.post("/generate_flyer")
def generate_flyer(req: FlyerRequest):
    matched_images = match_images(req.prompt)
    output_file = os.path.join(OUTPUT_DIR, f"flyer_{uuid.uuid4().hex}.jpg")
    create_flyer(matched_images, req.custom_text, output_file)
    return FileResponse(
        output_file, media_type="image/jpeg", filename=os.path.basename(output_file)
    )
