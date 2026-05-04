from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

#for Local Development, use the following 2 line:
# client = MongoClient("mongodb://localhost:27017/")
# db = client["synthia_db"]

# for Production, use the following 3 line: 
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["synthia_DB"]


users = db["users"]

def format_user(doc):
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "password": doc.get("password"),
        "created_at": doc["created_at"].strftime("%d %b %Y")
    }

def create_user(name, email, hashed_password):
    if users.find_one({"email": email}):
        return None
    doc = {"name": name, "email": email, "password": hashed_password, "created_at": datetime.utcnow()}
    result = users.insert_one(doc)
    return str(result.inserted_id)

def get_user_by_email(email):
    doc = users.find_one({"email": email})
    return format_user(doc) if doc else None

def get_user_by_id(user_id):
    try:
        doc = users.find_one({"_id": ObjectId(user_id)})
        return format_user(doc) if doc else None
    except:
        return None

def update_user(user_id, name):
    users.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": name}})
    return get_user_by_id(user_id)

def delete_user(user_id):
    result = users.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
