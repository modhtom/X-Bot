from dotenv import load_dotenv

load_dotenv()
import schedule
import time
from threading import Thread

from Quran import quran_main
from Dua import dua_main
from Image import image_main
from Hadith import h_main
from Other import other_main
from Friday import fr_main

from Helpers import TweetClient, Email, Live


bot = TweetClient.TwitterBot()
error_handler = Email.ErrorHandler()

azkar_tweeter = dua_main.AzkarTweeter(bot)
friday_tweeter = fr_main.FridayTweeter(bot)


def run_threaded(job_func, *args):
    job_thread = Thread(target=job_func, args=args)
    job_thread.start()


def safe_run(job_func, *args):
    try:
        run_threaded(job_func, *args)
    except Exception as e:
        error_handler.handle_error(
            e,
            f"A critical error occurred in the scheduler for job: {job_func.__name__}",
        )


print("🕒 Scheduling jobs...")

# 1. Frequent tasks (run about 3-4-6 times per hour)
schedule.every(3).hours.do(safe_run, quran_main.tweet_quran_verse, bot)
schedule.every(4).hours.do(safe_run, azkar_tweeter.tweet_azkar)
schedule.every(6).hours.do(safe_run, other_main.tweet_names_of_allah, bot)

# 2. Tasks to run twice a day (every 12 hours)
schedule.every(12).hours.do(safe_run, other_main.tweet_blogs, bot)
schedule.every(12).hours.do(
    safe_run, quran_main.tweet_random_ayah_with_explanation, bot
)
schedule.every(12).hours.do(safe_run, other_main.tweet_fatwas, bot)
schedule.every(12).hours.do(safe_run, h_main.getHadithFromBukhari, bot)
schedule.every(12).hours.do(safe_run, image_main.tweet_images, bot)

# 3. Tasks to run once a day at specific times in Egypt's timezone
schedule.every().day.at("08:00", "Africa/Cairo").do(
    safe_run, other_main.tweet_islamic_inspirations, bot
)
schedule.every().day.at("10:00", "Africa/Cairo").do(
    safe_run, other_main.tweet_islamic_calendar_reminders, bot
)
schedule.every().day.at("12:00", "Africa/Cairo").do(
    safe_run, other_main.tweet_islamic_challenges, bot
)
schedule.every().day.at("16:00", "Africa/Cairo").do(
    safe_run, other_main.tweet_prophetic_stories, bot
)

# 4. Special Friday tasks, also in Egypt's timezone
schedule.every().friday.at("07:00", "Africa/Cairo").do(
    safe_run, friday_tweeter.tweet_friday_introduction
)
schedule.every().friday.at("09:00", "Africa/Cairo").do(
    safe_run, friday_tweeter.tweet_alkahf_reminder
)

# The following will run every 2 hours *only on Fridays*
schedule.every(2).hours.do(safe_run, friday_tweeter.tweet_friday_sala)
# Run frequently on Friday afternoons.
schedule.every(15).minutes.do(safe_run, friday_tweeter.tweet_friday_dua)


def main():
    Live.keep_alive()
    print("🤖 Bot is alive and running scheduled jobs...")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_handler.handle_error(
            e, "A fatal error occurred in the main application loop"
        )
