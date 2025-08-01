import random
from Helpers import TweetClient, content


class AzkarTweeter:
    def __init__(self, bot: TweetClient.TwitterBot):
        self.bot = bot
        self.azkar_list = content.azkar_list
        random.shuffle(self.azkar_list)
        self.index = 0

    def tweet_azkar(self):
        if self.index >= len(self.azkar_list):
            self.index = 0
            random.shuffle(self.azkar_list)
            print("Azkar list exhausted. Reshuffling for new cycle.")

        content = self.azkar_list[self.index]
        tweet_content = f"🤲 {content}\n\n📿 #دعاء #ذكر"

        self.bot.tweet(tweet_content)

        self.index += 1
