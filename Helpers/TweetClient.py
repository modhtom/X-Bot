import os
import time
import requests
import tweepy
import tempfile
from functools import wraps
from Helpers import Data, Email

error_handler = Email.ErrorHandler()


def _handle_api_errors(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except tweepy.errors.TweepyException as e:
            if e.api_codes and 433 in e.api_codes:
                print("Skipping duplicate content.")
                return
            elif e.api_codes and 429 in e.api_codes:
                print("Rate limit exceeded. Waiting for 15 minutes before retrying...")
                time.sleep(15 * 60)
                return func(self, *args, **kwargs)
            else:
                error_handler.handle_error(
                    e, f"A Twitter API error occurred in {func.__name__}"
                )
        except Exception as e:
            print(e)   
            #error_handler.handle_error(
            #   e, f"An unexpected error occurred in {func.__name__}"
            #)

    return wrapper


class TwitterBot:
    def __init__(self):
        def _load_secret(var_name: str) -> str:
            file_path = f"/etc/secrets/{var_name}"
            if os.path.isfile(file_path):
                return open(file_path, "r").read().strip()
            try:
                return os.environ[var_name]
            except KeyError:
                raise ValueError(f"Missing credential: {var_name}")

        consumer_key = _load_secret("CONSUMER_KEY")
        consumer_secret = _load_secret("CONSUMER_SECRET")
        access_token = _load_secret("ACCESS_TOKEN")
        access_secret = _load_secret("ACCESS_SECRET")

        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )

        self.auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(self.auth)
        self.dry_run = os.getenv("DRY_RUN", "False").lower() in ("true", "1")

        if self.dry_run:
            print("🟢 BOT IS IN DRY RUN MODE. NO TWEETS WILL BE SENT. 🟢")

        print("TwitterBot initialized successfully.")

    @_handle_api_errors
    def tweet(self, tweet_text: str):
        if self.dry_run:
            print("--- 🌵 DRY RUN - TWEET 🌵 ---")
            print(tweet_text)
            print("------------------------------")
            return

        if len(tweet_text) <= 280:
            response = self.client.create_tweet(text=tweet_text)
            print(f"Tweeted: {response.data['id']}")
        else:
            self.tweet_thread(tweet_text)

    @_handle_api_errors
    def tweet_thread(self, tweet_text: str):
        chunks = Data.split_long_sentence(tweet_text)
        if self.dry_run:
            print("--- 🌵 DRY RUN - THREAD 🌵 ---")
            for i, chunk in enumerate(chunks):
                print(f"Part {i+1}/{len(chunks)}:\n{chunk}")
            print("-------------------------------")
            return
        main_tweet_id = None
        for i, chunk in enumerate(chunks):
            if i == 0:
                response = self.client.create_tweet(text=chunk)
                main_tweet_id = response.data["id"]
                print(f"Tweeted thread part 1: {main_tweet_id}")
            else:
                response = self.client.create_tweet(
                    text=chunk, in_reply_to_tweet_id=main_tweet_id
                )
                main_tweet_id = response.data["id"]
                print(f"Tweeted thread part {i+1}: {main_tweet_id}")

    @_handle_api_errors
    def i_tweet(self, link: str, status: str = ""):
        if self.dry_run:
            print("--- 🌵 DRY RUN - IMAGE TWEET 🌵 ---")
            print(f"Status: {status}")
            print(f"Image URL: {link}")
            print("-----------------------------------")
            return
        response = requests.get(link)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as temp_file:
            temp_file.write(response.content)
            media = self.api.media_upload(filename=temp_file.name)
            self.client.create_tweet(text=status, media_ids=[media.media_id])
            print(f"Tweeted image: {link}")

    @_handle_api_errors
    def v_tweet(self, status, video_path):
        # TODO: ADD Video tweeting
        error_handler.handle_error(0, f"An unexpected error occurred in v_tweet method")
