from pymongo import MongoClient
import os
from dotenv import load_dotenv
# from flask_cors import CORS

# CORS(app)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

DB_NAME = os.getenv("DB_NAME", "keyword_processor_db")

if not MONGO_URI:
    raise Exception("MONGO_URI not set. Check your .env file and ensure dotenv is installed.")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
laptops_collection = db["laptops"] # This collection stores the laptops associated with requests


# # Define your static image URLs (served by Flask)
# image_set = [
#     "http://127.0.0.1:5000/static/1/main.jpeg",
#     "http://127.0.0.1:5000/static/1/side_view.jpeg",
#     "http://127.0.0.1:5000/static/1/top_view.jpeg",
#     "http://127.0.0.1:5000/static/1/close_up.jpeg",
#     "http://127.0.0.1:5000/static/1/table_view.jpeg"
# ]

# Update every document in the collection
# result = laptops_collection.update_many({"images": {"$exists": False}}, {"$set": {"images": image_set}})
result = laptops_collection.delete_many({"cpu":{"$exists": False}})

# result = laptops_collection.delete_many({"cpu": "N/A"})
print(f"✅ Deleted {result.deleted_count} documents with CPU='N/A'")

