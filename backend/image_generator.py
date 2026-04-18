import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

TEXT2IMG_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
IMG2IMG_URL  = "https://router.huggingface.co/hf-inference/models/timbrooks/instruct-pix2pix"

ASPECT_RATIOS = {
    "1:1":  (1024, 1024),
    "16:9": (1024, 576),
    "9:16": (576, 1024),
    "4:3":  (1024, 768),
    "3:2":  (1024, 683),
}

def generate_image(prompt: str, aspect_ratio: str = "1:1") -> str:
    width, height = ASPECT_RATIOS.get(aspect_ratio, (1024, 1024))
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"width": width, "height": height}
    }
    try:
        response = requests.post(TEXT2IMG_URL, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode("utf-8")
    except requests.exceptions.Timeout:
        return None
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
    try:
        response = requests.post(IMG2IMG_URL, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode("utf-8")
    except requests.exceptions.Timeout:
        return None
    return None