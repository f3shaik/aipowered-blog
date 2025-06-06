import os
import json
import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from seo_fetcher import fetch_metrics
from ai_generator import generate_post
import zoneinfo

load_dotenv()

API_KEY= os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY not present in environment, use valid key and try again")

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello world!"

# API call to handle GET request "/generate", 
@app.route("/generate", methods=["GET"])
def generate_endpoint():
    keyword = request.args.get("keyword", "").strip()
    if not keyword: # when user didn't pass in "?keyword=..."
        return jsonify({"error" : "No keyword parameter provided"}), 400
    metrics = fetch_metrics(keyword) # Fetching mock SEO metrics, search_volume, keyword_difficulty, avg_cpc
    # generating post with OpenAI
    try:
        content = generate_post(keyword, metrics, api_key=API_KEY)
    except Exception as e:
        return jsonify({"error" : f"OpenAI API error: {str(e)}"}), 400
    save_to_file(keyword, content)
    response = {
        "keyword": keyword,
        "metrics": metrics,
        "content": content
    }
    return jsonify(response), 200  # success

# to run daily
def daily_job():
    set_keyword = "car pressure washer"
    metrics = fetch_metrics(set_keyword)
    try:
        content = generate_post(set_keyword, metrics, api_key=API_KEY)
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ERROR generating post: {e}")
        return 
    # Generate a file now saying that we successfuly ran a job
    save_to_file(set_keyword, content)

def save_to_file(keyword: str, content: str):
    day_str = datetime.datetime.now().strftime("%m%d%Y")
    filename = f"{keyword.replace(' ','_')}_{day_str}.md"
    out_dir = "generated_posts"
    os.makedirs(out_dir, exist_ok=True)
    dir_path = os.path.join(out_dir, filename)
    with open(dir_path, "w", encoding="utf-8") as file: # with automatically closes the file
        file.write(content)
    print(f"Saved daily post on [{datetime.datetime.now()}] to {dir_path}")


def scheduler():
    # Calling helper function to handle job run everyday
    scheduler = BackgroundScheduler(timezone="America/Los_Angeles")
    # Job will run on midnight
    scheduler.add_job(
        daily_job,
        trigger="cron",
        hour=1,
        minute=25,
        id="daily blog post",
        replace_existing=True
    )
    scheduler.start()
    print("[Scheduler] started for daily prompt at 00:00 PST")

if __name__ == "__main__":
    scheduler()
    app.run(host="0.0.0.0", port=6000, debug=True)