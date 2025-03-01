from Helpers import TweetClient as client, Email as email
import requests
import traceback
import re

API_URL = "https://raw.githubusercontent.com/nawafalqari/azkar-api/56df51279ab6eb86dc2f6202c7de26c8948331c1/azkar.json"
index = 0


def fetch_api_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        email.send(f"Failed to fetch data from {API_URL}")
        return None


def clean_tweet_content(text):
    cleaned_text = re.sub(r"\\n',\s*'|\\n',|\\n", " ", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text.strip()


def tweet_azkar():
    global index
    api_data = fetch_api_data()
    if not api_data:
        return

    filtered_data = {
        "أدعية قرآنية": api_data.get("أدعية قرآنية", []),
        "أدعية الأنبياء": api_data.get("أدعية الأنبياء", []),
        "تسابيح": api_data.get("تسابيح", []),
    }

    twitter_bot = client.TwitterBot()
    try:
        flat_data = [
            item["content"]
            for category in filtered_data.values()
            for sublist in category
            for item in (sublist if isinstance(sublist, list) else [sublist])
        ]

        if index < len(flat_data):
            text = flat_data[index]
            content = clean_tweet_content(text.strip())
            hashtag = "📿 #دعاء"
            tweet_content = f"🤲 {content} {hashtag}"
            if len(tweet_content) <= 270:
                # email.send(clean_tweet_content(f"{tweet_content} 💭 شاركونا بدعائكم 🙏"))
                twitter_bot.tweet(
                    clean_tweet_content(f"{tweet_content} 💭 شاركونا بدعائكم 🙏")
                )
            else:
                twitter_bot.tweet_thread(
                    clean_tweet_content(
                        f"📌 هذه سلسلة أدعية، تابعوا معنا. {tweet_content}"
                    )
                )
                # email.send(clean_tweet_content(f"{tweet_content} 💭 شاركونا بدعائكم 🙏"))
            index = (index + 1) % len(flat_data)
        else:
            email.send("All azkar have been tweeted.")
            index = 0
    except Exception as e:
        error_message = (
            f"An error occurred while tweeting azkar.\n"
            f"Index: {index}\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        email.send(error_message)
