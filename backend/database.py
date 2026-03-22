from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["synthia_db"]
collection = db["generations"]

def save_generation(original_prompt, expanded_prompt, style, image_base64, parent_id=None):
    doc = {
        "original_prompt": original_prompt,
        "expanded_prompt": expanded_prompt,
        "style": style,
        "image_base64": image_base64,
        "created_at": datetime.utcnow(),
        "parent_id": parent_id,
        "is_edit": parent_id is not None
    }
    result = collection.insert_one(doc)
    return str(result.inserted_id)

def format_doc(doc):
    return {
        "id": str(doc["_id"]),
        "original_prompt": doc["original_prompt"],
        "expanded_prompt": doc["expanded_prompt"],
        "style": doc["style"],
        "image_base64": doc["image_base64"],
        "created_at": doc["created_at"].strftime("%d %b %Y, %I:%M %p"),
        "parent_id": doc.get("parent_id"),
        "is_edit": doc.get("is_edit", False)
    }

def get_all_generations():
    # Fetch originals (no parent_id)
    originals = list(collection.find({"parent_id": None}).sort("created_at", -1))
    result = []
    for doc in originals:
        entry = format_doc(doc)
        # Fetch all edits for this original
        edits = list(collection.find({"parent_id": str(doc["_id"])}).sort("created_at", 1))
        entry["edits"] = [format_doc(e) for e in edits]
        result.append(entry)
    return result

def delete_generation(id: str):
    # Also delete all edits that belong to this original
    collection.delete_many({"parent_id": id})
    result = collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

def delete_edit(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

def get_generation_by_id(id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    return format_doc(doc) if doc else None