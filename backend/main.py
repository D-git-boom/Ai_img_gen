from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from style_modifier import apply_style
from prompt_intelligence import expand_prompt
from safety_filter import check_safety
from image_generator import generate_image, generate_image_edit
from database import save_generation, get_all_generations, delete_generation, delete_edit, get_generation_by_id, delete_user_generations
from auth import hash_password, verify_password, create_token, decode_token
from users_db import create_user, get_user_by_email, get_user_by_id, update_user, delete_user

app = FastAPI(title="Smart AI Image Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return None
    return get_user_by_id(user_id)

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UpdateRequest(BaseModel):
    name: str
    email: str

@app.post("/auth/signup")
def signup(req: SignupRequest):
    if len(req.password) < 6:
        return {"error": "Password must be at least 6 characters."}
    hashed = hash_password(req.password)
    user_id = create_user(req.name, req.email, hashed)
    if not user_id:
        return {"error": "An account with this email already exists."}
    token = create_token(user_id)
    user = get_user_by_id(user_id)
    return {"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"], "created_at": user["created_at"]}}

@app.post("/auth/login")
def login(req: LoginRequest):
    user = get_user_by_email(req.email)
    if not user or not verify_password(req.password, user["password"]):
        return {"error": "Invalid email or password."}
    token = create_token(user["id"])
    return {"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"], "created_at": user["created_at"]}}

@app.get("/auth/me")
def me(authorization: str = Header(None)):
    user = get_current_user(authorization)
    if not user:
        return {"error": "Unauthorized"}
    return {"id": user["id"], "name": user["name"], "email": user["email"], "created_at": user["created_at"]}

@app.put("/auth/update")
def update_profile(req: UpdateRequest, authorization: str = Header(None)):
    user = get_current_user(authorization)
    if not user:
        return {"error": "Unauthorized"}
    updated = update_user(user["id"], req.name, req.email)
    return {"user": {"id": updated["id"], "name": updated["name"], "email": updated["email"], "created_at": updated["created_at"]}}

@app.delete("/auth/delete")
def delete_account(authorization: str = Header(None)):
    user = get_current_user(authorization)
    if not user:
        return {"error": "Unauthorized"}
    delete_user_generations(user["id"])
    delete_user(user["id"])
    return {"success": True}

class GenerateRequest(BaseModel):
    prompt: str
    style: str = "realistic"
    aspect_ratio: str = "1:1"
    parent_id: Optional[str] = None
    original_image_base64: Optional[str] = None

@app.get("/")
def root():
    return {"status": "SYNTHIA backend running ✅"}

@app.post("/generate")
def generate(req: GenerateRequest, authorization: str = Header(None)):
    user = get_current_user(authorization)
    if not user:
        return {"error": "Unauthorized. Please log in."}
    if len(req.prompt) > 400:
        return {"error": "Prompt too long. Max 400 characters."}
    safety = check_safety(req.prompt)
    if not safety["safe"]:
        return {
            "error": "Prompt blocked by safety filter.",
            "triggered_keywords": safety["triggered"]
        }
    expanded = expand_prompt(req.prompt)
    styled_prompt = apply_style(expanded, req.style)
    is_edit = req.parent_id is not None and req.original_image_base64 is not None
    if is_edit:
        image_base64 = generate_image_edit(styled_prompt, req.original_image_base64)
        if not image_base64:
            parent = get_generation_by_id(req.parent_id)
            if parent:
                blended = f"{parent['expanded_prompt']}. Changes: {expanded}"
                image_base64 = generate_image(blended, req.aspect_ratio)
    else:
        image_base64 = generate_image(styled_prompt, req.aspect_ratio)
    if not image_base64:
        return {"error": "Image generation failed. Try again."}
    doc_id = save_generation(req.prompt, expanded, req.style, image_base64, req.aspect_ratio, req.parent_id, user["id"])
    return {
        "id": doc_id,
        "original_prompt": req.prompt,
        "expanded_prompt": expanded,
        "styled_prompt": styled_prompt,
        "aspect_ratio": req.aspect_ratio,
        "image_base64": image_base64,
        "is_edit": is_edit
    }

@app.get("/history")
def history(authorization: str = Header(None)):
    user = get_current_user(authorization)
    if not user:
        return {"error": "Unauthorized"}
    return get_all_generations(user["id"])

@app.get("/history/{id}")
def get_one(id: str):
    item = get_generation_by_id(id)
    return item if item else {"error": "Not found"}

@app.delete("/history/{id}")
def delete(id: str, authorization: str = Header(None)):
    user = get_current_user(authorization)
    if not user:
        return {"error": "Unauthorized"}
    return {"success": delete_generation(id)}

@app.delete("/edit/{id}")
<<<<<<< Updated upstream
def delete_one_edit(id: str):
    success = delete_edit(id)
    return {"success": success}
=======
def delete_one_edit(id: str, authorization: str = Header(None)):
    user = get_current_user(authorization)
    if not user:
        return {"error": "Unauthorized"}
    return {"success": delete_edit(id)}
>>>>>>> Stashed changes
