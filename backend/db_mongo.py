from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

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

def store_initial_request(ip, keyword):
    """Stores the initial request and returns the new document's ID."""
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

def get_analytics_for_frontend(keyword):
    """Calculates simple analytics based on stored data."""
    
    # 1. Total Count
    total_requests = requests_collection.count_documents({})
    
    # 2. Count for the specific keyword
    keyword_count = requests_collection.count_documents({"keyword": keyword})
    
    # 3. Simple aggregation for average result length (more complex in a real app)
    # Using a simple Python loop for simplicity, but map-reduce/aggregation pipeline is better
    all_results = requests_collection.find({"bot_result": {"$ne": None}}, {"bot_result": 1})
    
    total_len = sum(len(doc.get("bot_result", "")) for doc in all_results)
    avg_length = total_len / total_requests if total_requests else 0
    
    return {
        "total_requests": total_requests,
        "keyword_specific_count": keyword_count,
        "average_result_length": round(avg_length, 2),
        "database_type": "MongoDB" # Context for frontend
    }

def store_laptop_recommendations(request_id, items):
    """Upserts each recommended laptop by model name and tags it with the request_id."""
    for item in items:
        doc = item.copy()
        doc["request_id"] = request_id  # Link to the original request
        
        # Use upsert: update if model exists, else insert, and ensure it always
        # updates the request_id to the most recent one.
        laptops_collection.update_one(
            {"model": doc["model"]},
            {"$set": doc},
            upsert=True
        )

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


print("MongoDB connection initialized.")
