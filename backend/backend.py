from flask import Flask, request, jsonify
from flask_cors import CORS
from Laptop_Bot import run_query, answers_to_query, QUESTIONNAIRE, ask_questionnaire
# We need to import the new function from db_mongo here
from db_mongo import (
    store_initial_request, 
    store_bot_response, 
    get_analytics_for_frontend,
    get_latest_laptop_recommendations # <-- NEW IMPORT
)

app = Flask(__name__)
CORS(app)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    user_ip = request.remote_addr
    if "answers" in data:
        query_str = answers_to_query(data["answers"])
        keyword = query_str
    elif "custom_query" in data:
        query_str = data["custom_query"]
        keyword = query_str
    else:
        return jsonify({"error": "No query provided"}), 400

    # Store initial request and get request_id
    request_id = store_initial_request(user_ip, keyword)

    # Get bot result (This produces the 5 recommendations in resp_json["items"])
    resp_json = run_query(query_str, return_json=True)

    # Store bot response
    store_bot_response(request_id, str(resp_json))

    # Store each laptop as a separate document (used by the new /laptops route)
    if "items" in resp_json:
        from db_mongo import store_laptop_recommendations
        # This stores the 5 items recommended by the bot, associated with request_id
        store_laptop_recommendations(request_id, resp_json["items"])

    # Return the full bot response to the frontend (it contains the summary/messages)
    return jsonify(resp_json)

# ----------------------------------------------------------------------
# FIX IS HERE: This route now fetches only the 5 recommended laptops
# ----------------------------------------------------------------------
@app.route("/laptops", methods=["GET"])
def get_laptops():
    # Use the new function to retrieve ONLY the 5 recommended laptops
    laptops = get_latest_laptop_recommendations()
    
    if not laptops:
        return jsonify({"message": "No recent recommendations available."}), 200

    # Convert ObjectId to string for JSON serialization
    # Assuming 'l' is the full laptop document from the DB
    for l in laptops:
        if "_id" in l:
            l["_id"] = str(l["_id"])
            
    # This now returns only the 5 recommended laptops to the frontend
    return jsonify(laptops)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)