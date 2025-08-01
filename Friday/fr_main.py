import random
import datetime
import pytz
from Helpers import TweetClient, content


class FridayTweeter:
    def __init__(self, bot: TweetClient.TwitterBot):
        self.bot = bot

    def _is_friday_afternoon(self):
        now = datetime.datetime.now(pytz.timezone("Africa/Cairo"))
        return now.weekday() == 4 and now.hour >= 15

    def tweet_friday_introduction(self):
        self.bot.tweet(random.choice(content.friday_intro))

    def tweet_alkahf_reminder(self):
        self.bot.i_tweet(
            "https://imgs.search.brave.com/dK5drzycq-jQ7f41UmtYRoLtI1LYKgDaC4Va9lxGAPA/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5lbHptYW5uZXdz/LmNvbS9pbWcvMTkv/MTEvMTUvMTU4NjUw/NDE0OTcyNzUxMDUu/cG5n",
            status=content.kahf_reminder,
        )

    def tweet_friday_sala(self):
        if datetime.datetime.now(pytz.timezone("Africa/Cairo")).weekday() != 4:
            return

        sala_tweet = random.choice(content.friday_sala)
        self.bot.tweet(f"ﷺ {sala_tweet}\n\n#يوم_الجمعة #الصلاة_على_النبي")

    def tweet_friday_dua(self):
        if self._is_friday_afternoon():
            dua_tweet = random.choice(content.friday_dua)
            self.bot.tweet(f"🤲 {dua_tweet}\n\n#ساعة_استجابة #يوم_الجمعة")
