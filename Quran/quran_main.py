import random
from Helpers import QuranData, TweetClient, Email, content

error_handler = Email.ErrorHandler()


def tweet_quran_verse(bot: TweetClient.TwitterBot):
    try:
        surah_num = random.randint(1, 114)
        total_verses = QuranData.get_total_verses(surah_num)
        verse_num = random.randint(1, total_verses)

        verse = QuranData.get_surah_text(
            surah_num, verse_num, edition="quran-simple"
        ).replace("\n", " ")

        if len(verse) <= 280:
            tweet = (
                f"📖 قال تعالى:\n﴿{verse}﴾\n\n"
                f"📌 سورة {content.surah_names[surah_num-1]} | الآية: {verse_num}\n"
                f"#تدبر #آية 🌟"
            )
            bot.tweet(tweet)
        else:
            print(
                f"skipped verse number {verse_num} from surah {content.surah_names[surah_num-1]} because it doesn't fit tweet limit."
            )

    except Exception as e:
        error_handler.handle_error(e, f"Failed to tweet Quran verse.")


def tweet_random_ayah_with_explanation(bot: TweetClient.TwitterBot):
    try:
        surah_number = random.randint(1, 114)
        data = QuranData.fetch_surah_with_translation(surah_number)

        if not data or len(data) < 2:
            print("Could not retrieve surah or its translation.")
            return

        original_text, explanations = data[0]["ayahs"], data[1]["ayahs"]

        if len(original_text) != len(explanations):
            print("Mismatch between ayahs and translations.")
            return

        random_ayah_index = random.randint(0, len(original_text) - 1)
        selected_ayah = original_text[random_ayah_index]
        explanation = explanations[random_ayah_index]

        ayah_number = selected_ayah["numberInSurah"]
        content = (
            f"📖 سورة {data[0]['englishName']} ({data[0]['name']})\n"
            f"📝 آية {ayah_number}: {selected_ayah['text']}\n"
            f"📚 تفسير ميسر: {explanation['text']}\n\n"
            f"#القرآن #تفسير_القرآن"
        )
        bot.tweet(content)

        print(f"Tweeted explanation for random Ayah {ayah_number}.")
    except Exception as e:
        error_handler.handle_error(e, "Failed to tweet random Ayah with explanation.")
