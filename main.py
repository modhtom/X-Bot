from dotenv import load_dotenv

load_dotenv()

import pytz
from threading import Thread
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

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

cairo_tz = pytz.timezone("Africa/Cairo")


def run_threaded(fn, *args):
    Thread(target=fn, args=args, daemon=True).start()


def safe_run(fn, *args):
    try:
        run_threaded(fn, *args)
    except Exception as e:
        error_handler.handle_error(
            e, f"A critical error occurred in job: {fn.__name__}"
        )


def main():
    Live.keep_alive()
    print("Scheduling tweet jobs with APScheduler...")

    scheduler = BackgroundScheduler(timezone=cairo_tz)

    # 1. Frequent tasks (every 3, 4, 6 hours)
    frequent = [
        ("interval", dict(hours=3), quran_main.tweet_quran_verse, [bot]),
        ("interval", dict(hours=4), azkar_tweeter.tweet_azkar, []),
        ("interval", dict(hours=6), other_main.tweet_names_of_allah, [bot]),
    ]

    # 2. Twice-daily (every 12 hours)
    twice_daily = [
        ("interval", dict(hours=12), other_main.tweet_blogs, [bot]),
        (
            "interval",
            dict(hours=12),
            quran_main.tweet_random_ayah_with_explanation,
            [bot],
        ),
        ("interval", dict(hours=12), other_main.tweet_fatwas, [bot]),
        ("interval", dict(hours=12), h_main.getHadithFromBukhari, [bot]),
        ("interval", dict(hours=12), image_main.tweet_images, [bot]),
    ]

    # 3. Once-daily at fixed Cairo times
    daily_cron = [
        ("cron", dict(hour=8, minute=0), other_main.tweet_islamic_inspirations, [bot]),
        (
            "cron",
            dict(hour=10, minute=0),
            other_main.tweet_islamic_calendar_reminders,
            [bot],
        ),
        ("cron", dict(hour=12, minute=0), other_main.tweet_islamic_challenges, [bot]),
        ("cron", dict(hour=16, minute=0), other_main.tweet_prophetic_stories, [bot]),
    ]

    # 4. Friday-only jobs
    friday = [
        (
            "cron",
            dict(day_of_week="fri", hour=7, minute=0),
            friday_tweeter.tweet_friday_introduction,
            [],
        ),
        (
            "cron",
            dict(day_of_week="fri", hour=9, minute=0),
            friday_tweeter.tweet_alkahf_reminder,
            [],
        ),
        (
            "cron",
            dict(day_of_week="fri", hour="*/2", minute=0),
            friday_tweeter.tweet_friday_sala,
            [],
        ),
        (
            "cron",
            dict(day_of_week="fri", minute="*/15"),
            friday_tweeter.tweet_friday_dua,
            [],
        ),
    ]

    def register(job_list):
        for kind, trig_args, fn, fn_args in job_list:
            if kind == "interval":
                scheduler.add_job(
                    safe_run, trigger="interval", args=[fn, *fn_args], **trig_args
                )
            else:
                cron_trig = CronTrigger(timezone=cairo_tz, **trig_args)
                scheduler.add_job(safe_run, trigger=cron_trig, args=[fn, *fn_args])

    for group in (frequent, twice_daily, daily_cron, friday):
        register(group)

    scheduler.start()
    print("All tweet jobs scheduled.")
    Email.ErrorHandler.email_scheduled_jobs(scheduler, error_handler)

    try:
        while True:
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_handler.handle_error(e, "Fatal error in main loop")
