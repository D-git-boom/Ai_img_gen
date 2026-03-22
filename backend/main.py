from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from style_modifier import apply_style
from prompt_intelligence import expand_prompt
from safety_filter import is_safe
from image_generator import generate_image
from database import save_generation, get_all_generations, delete_generation, delete_edit, get_generation_by_id

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
    parent_id: Optional[str] = None  # set when editing

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

    doc_id = save_generation(
        original_prompt=req.prompt,
        expanded_prompt=expanded,
        style=req.style,
        image_base64=image_base64,
        parent_id=req.parent_id
    )

    return {
        "id": doc_id,
        "original_prompt": req.prompt,
        "expanded_prompt": expanded,
        "styled_prompt": styled_prompt,
        "image_base64": image_base64,
        "is_edit": req.parent_id is not None
    }

@app.get("/history")
def history():
    return get_all_generations()

@app.get("/history/{id}")
def get_one(id: str):
    item = get_generation_by_id(id)
    if not item:
        return {"error": "Not found"}
    return item

@app.delete("/history/{id}")
def delete(id: str):
    success = delete_generation(id)
    return {"success": success}

@app.delete("/edit/{id}")
def delete_one_edit(id: str):
    success = delete_edit(id)
    return {"success": success}