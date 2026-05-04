import os
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

#for Local Development, use the following 2 line:
client = MongoClient("mongodb://localhost:27017/")
db = client["synthia_db"]
# for Production, use the following 3 line: 
# MONGO_URI = os.getenv("MONGO_URI")
# client = MongoClient(MONGO_URI)
# db = client["synthia_DB"]

collection = db["generations"]
def format_doc(doc):
    return {
        "id": str(doc["_id"]),
        "original_prompt": doc["original_prompt"],
        "expanded_prompt": doc["expanded_prompt"],
        "style": doc["style"],
        "aspect_ratio": doc.get("aspect_ratio", "1:1"),
        "image_base64": doc["image_base64"],
        "created_at": doc["created_at"].strftime("%d %b %Y, %I:%M %p"),
        "parent_id": doc.get("parent_id"),
        "is_edit": doc.get("is_edit", False)
    }

def save_generation(original_prompt, expanded_prompt, style, image_base64, aspect_ratio="1:1", parent_id=None, user_id=None):
    doc = {
        "original_prompt": original_prompt,
        "expanded_prompt": expanded_prompt,
        "style": style,
        "aspect_ratio": aspect_ratio,
        "image_base64": image_base64,
        "created_at": datetime.utcnow(),
        "parent_id": parent_id,
        "is_edit": parent_id is not None,
        "user_id": user_id
    }
    result = collection.insert_one(doc)
    return str(result.inserted_id)

def get_all_generations(user_id=None):
    query = {"parent_id": None}
    if user_id:
        query["user_id"] = user_id
    originals = list(collection.find(query).sort("created_at", -1))
    result = []
    for doc in originals:
        entry = format_doc(doc)
        edits = list(collection.find({"parent_id": str(doc["_id"])}).sort("created_at", 1))
        entry["edits"] = [format_doc(e) for e in edits]
        result.append(entry)
    return result

def delete_generation(id: str):
    collection.delete_many({"parent_id": id})
    result = collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

def delete_edit(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

def delete_user_generations(user_id: str):
    collection.delete_many({"user_id": user_id})

def get_generation_by_id(id: str):

    doc = collection.find_one({"_id": ObjectId(id)})
    return format_doc(doc) if doc else None

    try:
        doc = collection.find_one({"_id": ObjectId(id)})
        return format_doc(doc) if doc else None
    except:
        return None

