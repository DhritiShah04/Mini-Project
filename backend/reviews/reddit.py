# reddit.py
import praw
import json
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), 'reviews.env')
load_dotenv(dotenv_path)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ensure json_files folder exists
os.makedirs(os.path.join(BASE_DIR, "reviews", "json_files"), exist_ok=True)


# Reddit API setup
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

def scrape_reddit_reviews(model_name, subreddit="laptops", limit=50):
    if "review" not in model_name.lower():
        model_name += " review"
    cache_dir = os.path.join(BASE_DIR, "reviews", "json_files", "reddit", "raw_reviews")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{model_name.replace(' ', '_')}.json")

    # If cached file exists, return cached reviews
    if os.path.exists(cache_path):
        print(f"♻️ Loading cached Reddit reviews for model: {model_name}")
        with open(cache_path, "r", encoding="utf-8") as f:
            cached_reviews = json.load(f)
        return cached_reviews

    reviews = []
    query = model_name
    for submission in reddit.subreddit(subreddit).search(query, limit=limit):
        text = submission.title + " " + submission.selftext
        reviews.append(text)
        
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            reviews.append(comment.body)
    
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved Reddit reviews to cache: {cache_path}")

    return reviews

if __name__ == "__main__":
    model_name = "IdeaPad Slim 3"
    reviews = scrape_reddit_reviews(model_name)