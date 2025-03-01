from Helpers import TweetClient as client, Email as email
import requests
import traceback
import random

bot = client.TwitterBot()
B_HADITH_RANGE = (1, 7008)


def getHadithFromBukhari():
    try:
        hadith_number = random.randint(*B_HADITH_RANGE)
        endpoint = f"https://api.hadith.gading.dev/books/bukhari/{hadith_number}"
        response = requests.get(endpoint)

        if response.status_code != 200:
            email.send(f"Failed to fetch hadith. Status code: {response.status_code}")
            return

        data = response.json().get("data")
        if not data:
            email.send(f"Invalid data format in response: {response.json()}")
            return

        hadith_text = data["contents"]["arab"]
        book_id = data["id"]
        hadith_number = data["contents"]["number"]

        # email.send(f"{hadith_text}\n{book_id} | {hadith_number}")

        tweet_content = (
            f"📜 قال رسول الله ﷺ:\n{hadith_text}\n\n"
            f"📚 {book_id} | رقم الحديث: {hadith_number}\n"
            f"📥 شارك هذا الحديث مع من تحب ❤️ #حديث_شريف"
        )

        if len(hadith_text) <= 260:
            bot.tweet(tweet_content)
        else:
            bot.tweet_thread(tweet_content)

    except Exception as e:
        error_message = (
            f"An error occurred in getHadithFromBukhari:\n"
            f"Hadith number: {hadith_number}\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        email.send(error_message)
