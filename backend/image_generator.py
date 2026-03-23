import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

TEXT2IMG_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
IMG2IMG_URL  = "https://router.huggingface.co/hf-inference/models/timbrooks/instruct-pix2pix"

def generate_image(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(TEXT2IMG_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return base64.b64encode(response.content).decode("utf-8")
    return None

def generate_image_edit(edit_prompt: str, original_image_base64: str) -> str:
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": original_image_base64,
        "parameters": {
            "prompt": edit_prompt,
            "num_inference_steps": 20,
            "image_guidance_scale": 1.5,
            "guidance_scale": 7.5
        }
    }
    response = requests.post(IMG2IMG_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode("utf-8")
    # Fallback: blend original prompt context into text2img if img2img fails
    return None