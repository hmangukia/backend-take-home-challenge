from fastapi import APIRouter
from models import FlyerRequest
import os
import openai
import base64

router = APIRouter()

ASSETS_DIR = "assets"

def encode_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

@router.post("/generate_flyer")
def generate_flyer(req: FlyerRequest):
    """
    Generates a flyer image based on the prompt and the product images provided.
    Example prompt: Design a clean, modern promotional image for our upcoming sale. Match the visual theme and tone of the product images provided. Use soft pastel tones and minimal layout. Do not add any text in the image.
    Args:
        req: FlyerRequest
    """
    prompt = req.prompt
    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key)

    image_extensions = (".png", ".gif", ".jpeg", ".webp")
    image_paths = [
        os.path.join(ASSETS_DIR, fname)
        for fname in os.listdir(ASSETS_DIR)
        if fname.lower().endswith(image_extensions)
    ]

    content = [{"type": "input_text", "text": prompt}]

    for img_path in image_paths:
        base64_img = encode_image(img_path)
        content.append({
            "type": "input_image",
            "image_url": f"data:image/png;base64,{base64_img}"
        })

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": content
            }
        ],
        tools=[
            {
                "type": "image_generation"
            }
        ],
    )

    image_generation_calls = [
        output
        for output in response.output
        if output.type == "image_generation_call"
    ]

    image_data = [output.result for output in image_generation_calls]

    if image_data:
        image_base64 = image_data[0]
        with open("flyer.png", "wb") as f:
            f.write(base64.b64decode(image_base64))
            print("Flyer saved as flyer.png")
    else:
        print(response.output.content)