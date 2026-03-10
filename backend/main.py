from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from style_modifier import apply_style
from prompt_intelligence import expand_prompt
from safety_filter import is_safe
from image_generator import generate_image

app = FastAPI(title="Smart AI Image Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str
    style: str = "realistic"

@app.get("/")
def root():
    return {"status": "Backend is running ✅"}

@app.post("/generate")
def generate(req: GenerateRequest):
    if not is_safe(req.prompt):
        return {"error": "Prompt blocked by safety filter. Please try a different prompt."}

    expanded = expand_prompt(req.prompt)
    styled_prompt = apply_style(expanded, req.style)
    image_base64 = generate_image(styled_prompt)

    if not image_base64:
        return {"error": "Image generation failed. Try again."}

    return {
        "original_prompt": req.prompt,
        "expanded_prompt": expanded,
        "styled_prompt": styled_prompt,
        "image_base64": image_base64
    }