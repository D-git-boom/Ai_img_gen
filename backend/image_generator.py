import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

def generate_image(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return base64.b64encode(response.content).decode("utf-8")
    else:
        return None