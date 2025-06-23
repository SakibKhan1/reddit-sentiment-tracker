from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import praw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import re

#loads env variables for private details 
load_dotenv()

app = Flask(__name__)

#Reddit API Config (from .env) 
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = "keyword-sentiment-analyzer by /u/No-Mine-3982"
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD
)

#My list of slang words with positive/negative connotations..
#..these are the words that I see most frequently as an active r/nba user of 7 years.
positive_words = [
    "great", "amazing", "goat", "legend", "love", "best", "fantastic",
    "elite", "clutch", "beast", "unstoppable", "dominant",
    "excellent", "fire", "insane", "unbelievable", "crazy", "iconic", "legendary",
    "good", "solid", "consistent", "ethical", "smart", "high basketball iq"

]

negative_words = [
    "overrated", "trash", "washed", "hate", "bad", "terrible",
    "worst", "scrub", "soft", "choker", "liability",
    "garbage", "bum", "fraud", "brick", "sellout", "lazy", "injury-prone",
    "flopper", "foul bait", "don't like", "boring", "stupid", "useless", 
    "no basketball iq", "idiot"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subreddit_name = request.form['subreddit'] or 'nba'
        keyword = request.form['keyword'].lower()

        total_mentions = 0
        positive_mentions = 0
        negative_mentions = 0
        positive_words_found = set()
        negative_words_found = set()

        #allows flexible patterns 
        pattern = re.compile(rf"{re.escape(keyword)}[-’' ]?", re.IGNORECASE)

        #Fetch 30 HOT posts only
        posts = []
        seen_ids = set()

        for s in reddit.subreddit(subreddit_name).hot(limit=50):
            if not s.stickied and s.id not in seen_ids:
                posts.append(s)
                seen_ids.add(s.id)
            if len(posts) >= 30:
                break

        #Analyze posts + all comments (unlimited depth) 
        #By making all comments allows negative upvoted comments to take part in analysis
        for submission in posts:
            text = f"{submission.title} {submission.selftext}".lower()

            if pattern.search(text):
                total_mentions += 1
                for word in positive_words:
                    if word in text:
                        positive_mentions += 1
                        positive_words_found.add(word)
                        break
                for word in negative_words:
                    if word in text:
                        negative_mentions += 1
                        negative_words_found.add(word)
                        break

            try:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    comment_text = comment.body.lower()
                    if pattern.search(comment_text):
                        total_mentions += 1
                        for word in positive_words:
                            if word in comment_text:
                                positive_mentions += 1
                                positive_words_found.add(word)
                                break
                        for word in negative_words:
                            if word in comment_text:
                                negative_mentions += 1
                                negative_words_found.add(word)
                                break
            except Exception as e:
                print(f"Skipping comments due to error: {e}")
                continue

        #Create bar chart for visualization 
        labels = ['Total', 'Positive', 'Negative']
        counts = [total_mentions, positive_mentions, negative_mentions]

        fig, ax = plt.subplots()
        ax.bar(labels, counts, color=['blue', 'green', 'red'])
        ax.set_title(f"Mentions of '{keyword}' in r/{subreddit_name}")
        ax.set_ylabel("Count")

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)

        return render_template(
            'result.html',
            keyword=keyword,
            subreddit=subreddit_name,
            total=total_mentions,
            positive=positive_mentions,
            positive_words=list(positive_words_found),
            negative=negative_mentions,
            negative_words=list(negative_words_found),
            plot_url=plot_url
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
