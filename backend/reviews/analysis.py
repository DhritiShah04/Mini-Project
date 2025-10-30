import os
import json
import concurrent.futures
import time
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from keybert import KeyBERT
from transformers import pipeline


from reddit import scrape_reddit_reviews
from youtube import scrape_youtube_reviews

os.makedirs("json_files/reddit/analysis", exist_ok=True)
os.makedirs("json_files/youtube/analysis", exist_ok=True)


def clean_text(text):
    """Remove URLs, special characters, and extra whitespace."""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

user_keywords = {
    'Gamers': [
        'fps', 'game', 'gaming', 'gpu', 'twitch', 'stream', 'fortnite', 'csgo', 'valorant',
        'esports', 'high refresh rate', 'overclock', 'mmorpg', 'low latency', 'ray tracing'
    ],
    'Students': [
        'study', 'school', 'college', 'assignment', 'homework', 'lecture', 'project', 'exam', 'class',
        'research', 'zoom', 'online class', 'notes', 'presentation', 'group work', 'pdf', 'writing', 'report'
    ],
    'Content Creators': [
        'youtube', 'editing', 'video', 'render', 'streaming', 'photoshop', 'premiere', 'vlog',
        'after effects', 'color grading', 'audio mixing', 'graphic tablet', '1080p', '4k', 'animation', 'creative cloud'
    ],
    'Casual Users': [
        'internet', 'browsing', 'movies', 'netflix', 'social media', 'web', 'youtube', 'watching',
        'facebook', 'instagram', 'facebook', 'twitter', 'spotify', 'podcast', 'email', 'shopping'
    ],
    'Programmers / Engineers': [
        'coding', 'programming', 'python', 'java', 'software', 'developer', 'debug', 'compile',
        'engineer', 'data', 'linux', 'git', 'docker', 'algorithm', 'machine learning', 'api', 'script'
    ]
}

def classify_reviews_by_user(reviews, keywords_dict):
    categorized = {user: [] for user in keywords_dict.keys()}
    for review in reviews:
        review_lower = review.lower()
        for user, keywords in keywords_dict.items():
            if any(word in review_lower for word in keywords):
                categorized[user].append(review)
    return categorized

def analyze_sentiment(reviews, sia):
    pos = neg = neu = 0
    compound_total = 0
    for r in reviews:
        score = sia.polarity_scores(r)
        compound_total += score['compound']
        if score['compound'] >= 0.05:
            pos += 1
        elif score['compound'] <= -0.05:
            neg += 1
        else:
            neu += 1
    total = len(reviews)
    return {
        "positive": pos,
        "neutral": neu,
        "negative": neg,
        "total_reviews": total,
        "sentiment_score": round((pos - neg)/total, 3) if total else None,
        "avg_compound": round(compound_total/total, 3) if total else None
    }

sia = SentimentIntensityAnalyzer()
kw_model = KeyBERT('distilbert-base-nli-mean-tokens')

def load_analysis_cache(model_name, source):
    filename = f"{model_name.replace(' ', '_')}_analysis.json"
    filepath = os.path.join("json_files", source, "analysis", filename)
    if os.path.exists(filepath):
        print(f"♻️ Analysis cache exists for {model_name} [{source}], loading...")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_analysis_cache(model_name, source, analysis_data):
    filename = f"{model_name.replace(' ', '_')}_analysis.json"
    filepath = os.path.join("json_files", source, "analysis", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved combined analysis cache for {model_name} [{source}]")


# Initialize summarizer (load once outside the function)
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def analyze_reviews(reviews, sia, kw_model, user_keywords, model_name, source):
    clean_reviews = [clean_text(r) for r in reviews if len(r.strip()) > 20]
    user_categorized = classify_reviews_by_user(clean_reviews, user_keywords)

    cached_data = load_analysis_cache(model_name, source)
    if cached_data:
        return {
            "clean_reviews": clean_reviews,
            "reviews_by_user": user_categorized,
            "sentiment_by_user": cached_data.get("sentiment_by_user", {}),
            "keywords_by_user": cached_data.get("keywords_by_user", {}),
            # "summaries_by_user": cached_data.get("summaries_by_user", {}),  # commented out to skip summarization for now
            "example_snippets_by_user": cached_data.get("example_snippets_by_user", {})
        }

    sentiment_results = {}
    keywords_results = {}
    summaries = {}
    example_snippets = {}

    for user in user_keywords.keys():
        user_reviews = user_categorized.get(user, [])

        sentiment_results[user] = analyze_sentiment(user_reviews, sia)

        if user_reviews:
            all_text = " ".join(user_reviews)

            keywords = kw_model.extract_keywords(
                all_text,
                top_n=10,
                stop_words='english',
                keyphrase_ngram_range=(1, 3)
            )
            keywords_results[user] = [kw[0] for kw in keywords]

            # The summarization section is commented out to speed up processing
            # try:
            #     summarized = summarizer(all_text[:1000], max_length=60, min_length=25, do_sample=False)[0]['summary_text']
            #     summaries[user] = summarized
            # except Exception:
            #     summaries[user] = "Summary unavailable"

            pos_snips, neg_snips = [], []
            for review in user_reviews:
                score = sia.polarity_scores(review)['compound']
                if score >= 0.4 and len(pos_snips) < 3:
                    pos_snips.append(review)
                elif score <= -0.4 and len(neg_snips) < 3:
                    neg_snips.append(review)
                if len(pos_snips) >= 3 and len(neg_snips) >= 3:
                    break

            example_snippets[user] = {"positive": pos_snips, "negative": neg_snips}
        else:
            keywords_results[user] = []
            summaries[user] = ""
            example_snippets[user] = {"positive": [], "negative": []}

    combined_analysis = {
        "sentiment_by_user": sentiment_results,
        "keywords_by_user": keywords_results,
        # "summaries_by_user": summaries,  # commenting out summary saving as well
        "example_snippets_by_user": example_snippets
    }

    save_analysis_cache(model_name, source, combined_analysis)

    return {
        "clean_reviews": clean_reviews,
        "reviews_by_user": user_categorized,
        **combined_analysis
    }


def process_model(model_name):
    print(f"🔹 Processing model: {model_name}")
    start_model = time.time()

    os.makedirs("json_files/reddit", exist_ok=True)
    os.makedirs("json_files/youtube", exist_ok=True)

    start_fetch = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        reddit_future = executor.submit(scrape_reddit_reviews, model_name)
        youtube_future = executor.submit(scrape_youtube_reviews, model_name)
        reddit_reviews = reddit_future.result()
        youtube_reviews = youtube_future.result()
    end_fetch = time.time()

    # Parallel analyze_reviews for Reddit and YouTube
    start_analysis = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        reddit_analysis_future = executor.submit(analyze_reviews, reddit_reviews, sia, kw_model, user_keywords, model_name, "reddit")
        youtube_analysis_future = executor.submit(analyze_reviews, youtube_reviews, sia, kw_model, user_keywords, model_name, "youtube")
        reddit_analysis = reddit_analysis_future.result()
        youtube_analysis = youtube_analysis_future.result()
    end_analysis = time.time()

    output = {
        "model_name": model_name,
        "total_reviews_reddit": len(reddit_analysis["clean_reviews"]),
        "total_reviews_youtube": len(youtube_analysis["clean_reviews"]),
        "reviews_by_user_reddit": reddit_analysis["reviews_by_user"],
        "reviews_by_user_youtube": youtube_analysis["reviews_by_user"],
        "sentiment_reddit_by_user": reddit_analysis["sentiment_by_user"],
        "sentiment_youtube_by_user": youtube_analysis["sentiment_by_user"],
        "keywords_reddit_by_user": reddit_analysis["keywords_by_user"],
        "keywords_youtube_by_user": youtube_analysis["keywords_by_user"],
        "timings": {
            "fetch_time_sec": round(end_fetch - start_fetch, 2),
            "analysis_time_sec": round(end_analysis - start_analysis, 2),
            "total_time_sec": round(time.time() - start_model, 2)
        }
    }

    # combined_file = os.path.join("json_files", f"{model_name.replace(' ', '_')}_analysis.json")
    # with open(combined_file, "w", encoding="utf-8") as f:
    #     json.dump(output, f, ensure_ascii=False, indent=2)
    # print(f"✅ Combined analysis saved → {combined_file}")
    print(f"   Fetch Time: {output['timings']['fetch_time_sec']}s, "
          f"Analysis Time: {output['timings']['analysis_time_sec']}s, "
          f"Total Time: {output['timings']['total_time_sec']}s")
    return output

def process_models(models_list):
    all_outputs = []
    max_workers = min(len(models_list), 5)
    start_pipeline = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_model, model) for model in models_list]
        for f in concurrent.futures.as_completed(futures):
            all_outputs.append(f.result())
    end_pipeline = time.time()
    print(f"\n🚀 Pipeline completed for {len(models_list)} models in {round(end_pipeline - start_pipeline, 2)} seconds")
    return all_outputs

# Example run
if __name__ == "__main__":
    model_names = [
        "IdeaPad Slim 3",
        "IdeaPad Slim 5",
        "ThinkBook 14",
        "IdeaPad Flex 5",
        "ThinkPad E14"
    ]
    outputs = process_models(model_names)
