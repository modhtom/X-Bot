from Helpers import TweetClient as client, Email, content
import random

error_handler = Email.ErrorHandler()


def tweet_images():
    bot = client.TwitterBot()
    try:
        img = random.choice(content.links)
        bot.i_tweet(img)
    except Exception as e:
        error_handler.handle_error(e, "Failed while tweeting an image.")
