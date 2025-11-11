from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
# from Laptop_Bot import fetch_laptop_details

load_dotenv()

# FIX: Get the URI from environment. Do NOT use the localhost default.
MONGO_URI = os.getenv("MONGO_URI")

# FIX: Ensure DB_NAME is also read from .env if you set it there.
DB_NAME = os.getenv("DB_NAME", "keyword_processor_db")

# Safety check (Highly Recommended)
if not MONGO_URI:
    raise Exception("MONGO_URI not set. Check your .env file and ensure dotenv is installed.")


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
requests_collection = db["requests"]
laptops_collection = db["laptops"] # This collection stores the laptops associated with requests
users_collection = db["users"]

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto") 

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(username, password):
    if users_collection.find_one({"username": username}):
        return False, "Username already exists"
    
    hashed_pass = hash_password(password)
    user_data = {
        "username": username,
        "password": hashed_pass,
        "created_at": datetime.now()
    }
    result = users_collection.insert_one(user_data)
    return True, str(result.inserted_id)

def get_user_by_username(username):
    user = users_collection.find_one({"username": username})
    return user

def store_initial_request(ip, keyword):
    request_data = { 
        "ip_address": ip,
        "keyword": keyword,
        "timestamp": datetime.now(),
        "bot_result": None,
        "status": "pending"
    }
    result = requests_collection.insert_one(request_data)
    # MongoDB uses ObjectId for _id, convert it to string for easy use
    return str(result.inserted_id) 

def store_bot_response(request_id_str, bot_result):
    """Updates the request document with the bot's result."""
    requests_collection.update_one(
        {"_id": ObjectId(request_id_str)},
        {"$set": {"bot_result": bot_result, "status": "processed"}}
    )

# def get_analytics_for_frontend(keyword):
    
#     # 1. Total Count
#     total_requests = requests_collection.count_documents({})
    
#     # 2. Count for the specific keyword
#     keyword_count = requests_collection.count_documents({"keyword": keyword})
    
#     # 3. Simple aggregation for average result length (more complex in a real app)
#     # Using a simple Python loop for simplicity, but map-reduce/aggregation pipeline is better
#     all_results = requests_collection.find({"bot_result": {"$ne": None}}, {"bot_result": 1})
    
#     total_len = sum(len(doc.get("bot_result", "")) for doc in all_results)
#     avg_length = total_len / total_requests if total_requests else 0
    
#     return {
#         "total_requests": total_requests,
#         "keyword_specific_count": keyword_count,
#         "average_result_length": round(avg_length, 2),
#         "database_type": "MongoDB" # Context for frontend
#     }

# def store_laptop_recommendations(request_id, items):
#     """Upserts each recommended laptop by model name and tags it with the request_id."""
#     for item in items:
#         doc = item.copy()
#         doc["request_id"] = request_id  # Link to the original request
        
#         # Use upsert: update if model exists, else insert, and ensure it always
#         # updates the request_id to the most recent one.
#         laptops_collection.update_one(
#             {"model": doc["model"]},
#             {"$set": doc},
#             upsert=True
#         )

# def store_laptop_recommendations(request_id, items):

#     # folder_id = random.randint(1, 10)
#     # BASE_URL = f"http://127.0.0.1:5000/static/{folder_id}"

#     BASE_URL = "http://127.0.0.1:5000/static/1"
#     default_images = [
#         f"{BASE_URL}/main.jpeg",
#         f"{BASE_URL}/side_view.jpeg",
#         f"{BASE_URL}/top_view.jpeg",
#         f"{BASE_URL}/close_up.jpeg",
#         f"{BASE_URL}/table_view.jpeg"
#     ]

#     for item in items:
#         doc = item.copy()
#         doc["request_id"] = request_id

#         # If this laptop doesn't already have images, attach defaults
#         existing = laptops_collection.find_one({"model": doc["model"]}, {"images": 1})
#         if not existing or "images" not in existing:
#             doc["images"] = default_images

#         laptops_collection.update_one(
#             {"model": doc["model"]},
#             {"$set": doc},
#             upsert=True
#         )

# def store_laptop_recommendations(request_id, items):
#     from Laptop_Bot import fetch_laptop_details  # Local import to avoid circular dependency

#     BASE_URL = "http://127.0.0.1:5000/static/1"
#     default_images = [
#         f"{BASE_URL}/main.jpeg",
#         f"{BASE_URL}/side_view.jpeg",
#         f"{BASE_URL}/top_view.jpeg",
#         f"{BASE_URL}/close_up.jpeg",
#         f"{BASE_URL}/table_view.jpeg"
#     ]

#     new_models = []  # To store all models not in DB
#     item_map = {}    # To map model name → original item

#     # Step 1: Identify which models are new
#     for item in items:
#         doc = item.copy()
#         model = doc.get("model")

#         if not model:
#             print("Skipping item without model key")
#             continue

#         item_map[model] = doc  # Keep a reference for later
#         existing = laptops_collection.find_one({"model": model})

#         if not existing:
#             new_models.append({"model": model})

#     # Step 2: Fetch details for all new models (batch)
#     fetched_details = []
#     if new_models:
#         print(f"Fetching details for {len(new_models)} new models...")
#         try:
#             fetched_details = fetch_laptop_details(new_models)
#         except Exception as e:
#             print(f"Error fetching new laptop details: {e}")
#     else:
#         print("No new models to fetch.")

#     # Step 3: Build a lookup from fetched results
#     fetched_map = {}
#     if fetched_details:
#         for detail in fetched_details:
#             model_name = detail.get("model")
#             if model_name:
#                 fetched_map[model_name] = detail

#     # Step 4: Merge everything and upsert into DB
#     for model, doc in item_map.items():
#         existing = laptops_collection.find_one({"model": model})
#         if not existing:
#             # Merge fetched details if available
#             if model in fetched_map:
#                 doc.update(fetched_map[model])
#             else:
#                 print(f"No extra details found for {model}")

#             doc["images"] = default_images
#         else:
#             doc["images"] = existing.get("images", default_images)

#         doc["request_id"] = request_id

#         laptops_collection.update_one(
#             {"model": model},
#             {"$set": doc},
#             upsert=True
#         )

#     print("Laptop recommendations stored/updated successfully.")

def store_laptop_recommendations(request_id, items):
    from Laptop_Bot import fetch_laptop_details  # local import avoids circular dependency

    BASE_URL = "http://127.0.0.1:5000/static/1"
    default_images = [
        f"{BASE_URL}/main.jpeg",
        f"{BASE_URL}/side_view.jpeg",
        f"{BASE_URL}/top_view.jpeg",
        f"{BASE_URL}/close_up.jpeg",
        f"{BASE_URL}/table_view.jpeg"
    ]

    new_models = []
    item_map = {}

    # Step 1: Identify models that are not in DB
    for item in items:
        doc = item.copy()
        model = doc.get("model")

        if not model:
            print("Skipping item without model key")
            continue

        item_map[model] = doc
        existing = laptops_collection.find_one({"model": model})
        if not existing:
            new_models.append({"model": model})

    # Step 2: Fetch details for new models (batch request)
    fetched_details = []
    if new_models:
        print(f"\nFetching details for {len(new_models)} new models...")
        try:
            fetched_details = fetch_laptop_details(new_models, return_json=True)
            if not isinstance(fetched_details, list):
                print("⚠️ fetch_laptop_details did not return a list — wrapping result manually.")
                fetched_details = [fetched_details]
        except Exception as e:
            print(f"Error fetching laptop details: {e}")
    else:
        print("No new models to fetch.\n")

    # Step 3: Build a mapping from model → detailed specs
    fetched_map = {}
    for detail in fetched_details or []:
        model_name = detail.get("model")
        if model_name:
            fetched_map[model_name] = detail

    # Step 4: Merge fetched specs and upsert into DB
    added, updated = 0, 0

    for model, doc in item_map.items():
        existing = laptops_collection.find_one({"model": model})

        if not existing:
            extra = fetched_map.get(model)
            if extra:
                doc.update(extra)
                print(f"✅ Added detailed specs for: {model}")
            else:
                print(f"⚠️ No extra details found for {model}")

            doc["images"] = default_images
            added += 1
        else:
            doc["images"] = existing.get("images", default_images)
            updated += 1

        doc["request_id"] = request_id

        laptops_collection.update_one(
            {"model": model},
            {"$set": doc},
            upsert=True
        )

    print(f"\nLaptop recommendations stored/updated successfully.")
    print(f"📦 Added: {added}, 🔁 Updated: {updated}\n")


# --------------------------------------------------------------------------
# FIX: NEW REQUIRED FUNCTION TO SUPPORT THE /laptops GET ROUTE
# --------------------------------------------------------------------------
def get_latest_laptop_recommendations():
    """
    Retrieves the 5 laptop documents associated with the most recent 
    processed request ID. This ensures the frontend only sees the 
    laptops recommended by the bot.
    """
    
    # 1. Find the ID of the most recent PROCESSED request
    latest_request_doc = requests_collection.find_one(
        {"status": "processed"},
        sort=[('timestamp', -1)] # Find the document with the latest timestamp
    )
    
    if not latest_request_doc:
        return []

    latest_request_id = str(latest_request_doc["_id"])
    
    # 2. Retrieve all laptop documents matching that request ID
    # Since the bot limits results to 5 and store_laptop_recommendations updates 
    # the request_id, we look for laptops tagged with the latest request_id.
    
    # NOTE: Since multiple requests can share the same laptop model, we limit 
    # the find operation to 5, assuming the bot always recommends 5.
    recommended_laptops = list(laptops_collection.find(
        {"request_id": latest_request_id}
    ).limit(5))
    
    return recommended_laptops

def update_user_wishlist (user_id, model, action):
    try:
        user_oid = ObjectId(user_id)

        if(action == 'add') :
            users_collection.update_one(
                {"_id": user_oid},
                {"$addToSet": {"wishlist":model}},
            )
            return True, "Item in wishlist" 
            
        elif action == "remove" :
            update_res = users_collection.update_one(
                {"_id": user_oid},
                {"$pull": {"wishlist": model}},
            )
            return update_res.modified_count > 0, "Wishlist updated"
            
        else :
            return False, "Invalid Action"
    
    except Exception as e:
        print(f"Error updating wishlist: {e}")
        return False, str(e)
    
def get_wishlisted_laptops(user_id) :
    try: 
        user_oid = ObjectId(user_id)
        user_doc = users_collection.find_one(
            {"_id": user_oid},
            {"wishlist":1},
        )

        if not user_doc or "wishlist" not in user_doc:
            return []

        wishlist_models = user_doc.get('wishlist', [])
        wishlist_laptops = list(laptops_collection.find({
            "model": {"$in": wishlist_models}
        }))

        for laptop in wishlist_laptops:
            if '_id' in laptop:
                laptop['_id'] = str(laptop['_id'])

        return wishlist_laptops
    
    except Exception as e:
        print(f"Error fetching wishlist: {e}")
        return []

print("MongoDB connection initialized.")
