from threading import Thread
import traceback
import datetime
import pytz
import time
from Friday import fr_main as fri
from Quran import quran_main as quran
from Dua import dua_main as dua
from Image import image_main as image
from Hadith import h_main as hadith
from Other import other_main as other
from Helpers import Live as live, Email as email

TWEET_BREAK = 960  # 16 minutes
TWEET_BREAK_LONG = 10800  # 3 hours


def is_friday(now):
    return now.weekday() == 4


def execute_with_delay(function, delay=TWEET_BREAK):
    function()
    time.sleep(delay)


def handle_daily_tweets():
    tweetOncePerDay = None
    tweetTwicePerDay = None
    while True:
        try:
            now = datetime.datetime.now(pytz.utc).astimezone(
                pytz.timezone("Africa/Cairo")
            )

            if is_friday(now):
                fri.fri()
                fri.friday_sala_dua()

            tweet_functions = [
                quran.tweet_quran_verse,
                dua.tweet_azkar,
                other.tweet_names_of_allah,
            ]
            for func in tweet_functions:
                execute_with_delay(func)

            if not tweetTwicePerDay or (
                (now - tweetTwicePerDay).total_seconds() >= 12 * 60 * 60
            ):
                double_tweet_tasks = [
                    other.tweet_blogs,
                    quran.tweet_random_ayah_with_explanation,
                    other.tweet_fatwas,
                    hadith.getHadithFromBukhari,
                    image.tweet_images,
                ]
                for task in double_tweet_tasks:
                    execute_with_delay(task)
                tweetTwicePerDay = now

            if tweetOncePerDay != now.day:
                daily_tweet_tasks = [
                    other.tweet_islamic_inspirations,
                    other.tweet_islamic_calendar_reminders,
                    other.tweet_islamic_challenges,
                ]
                for task in daily_tweet_tasks:
                    execute_with_delay(task)
                tweetOncePerDay = now.day

            time.sleep(TWEET_BREAK_LONG)

        except Exception as e:
            error_message = (
                f"An error occurred during handle_daily_tweets execution:\n"
                f"Error Type: {type(e).__name__}\n"
                f"Error Message: {str(e)}\n"
                f"Traceback: {traceback.format_exc()}"
            )
            email.send(error_message)
            time.sleep(TWEET_BREAK)


if __name__ == "__main__":
    try:
        live.keep_alive()
        while True:
            Thread(target=live.run_server).start()
            handle_daily_tweets()
    except Exception as e:
        error_message = (
            f"An error occurred in the main loop:\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        email.send(error_message)
