import traceback
from Helpers import QuranData, TweetClient as client, Email as email
import random

surah_names = [
    "الفاتحة",
    "البقرة",
    "آل عمران",
    "النساء",
    "المائدة",
    "الأنعام",
    "الأعراف",
    "الأنفال",
    "التوبة",
    "يونس",
    "هود",
    "يوسف",
    "الرعد",
    "إبراهيم",
    "الحجر",
    "النحل",
    "الإسراء",
    "الكهف",
    "مريم",
    "طه",
    "الأنبياء",
    "الحج",
    "المؤمنون",
    "النور",
    "الفرقان",
    "الشعراء",
    "النمل",
    "القصص",
    "العنكبوت",
    "الروم",
    "لقمان",
    "السجدة",
    "الأحزاب",
    "سبأ",
    "فاطر",
    "يس",
    "الصافات",
    "ص",
    "الزمر",
    "غافر",
    "فصلت",
    "الشورى",
    "الزخرف",
    "الدخان",
    "الجاثية",
    "الأحقاف",
    "محمد",
    "الفتح",
    "الحجرات",
    "ق",
    "الذاريات",
    "الطور",
    "النجم",
    "القمر",
    "الرحمن",
    "الواقعة",
    "الحديد",
    "المجادلة",
    "الحشر",
    "الممتحنة",
    "الصف",
    "الجمعة",
    "المنافقون",
    "التغابن",
    "الطلاق",
    "التحريم",
    "الملك",
    "القلم",
    "الحاقة",
    "المعارج",
    "نوح",
    "الجن",
    "المزمل",
    "المدثر",
    "القيامة",
    "الإنسان",
    "المرسلات",
    "النبأ",
    "النازعات",
    "عبس",
    "التكوير",
    "الإنفطار",
    "المطففين",
    "الإنشقاق",
    "البروج",
    "الطارق",
    "الأعلى",
    "الغاشية",
    "الفجر",
    "البلد",
    "الشمس",
    "الليل",
    "الضحى",
    "الشرح",
    "التين",
    "العلق",
    "القدر",
    "البينة",
    "الزلزلة",
    "العاديات",
    "القارعة",
    "التكاثر",
    "العصر",
    "الهمزة",
    "الفيل",
    "قريش",
    "الماعون",
    "الكوثر",
    "الكافرون",
    "النصر",
    "المسد",
    "الإخلاص",
    "الفلق",
    "الناس",
]

bot = client.TwitterBot()


def tweet_quran_verse():
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
                f"📌 سورة {surah_names[surah_num-1]} | الآية: {verse_num}\n"
                f"#تدبر #آية 🌟"
            )
            bot.tweet(tweet)
            # print(f"tweeted: {tweet}")
        else:
            print(
                f"skipped verse number {verse_num} from surah {surah_names[surah_num-1]} because it doesn't fit tweet limit."
            )

    except Exception as e:
        error_message = (
            f"An error occurred while tweeting Quran verse.\n"
            f"Surah: {surah_num}, Verse: {verse_num}\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        print(error_message)
        email.send(error_message)


def tweet_random_ayah_with_explanation():
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
        error_message = (
            f"An error occurred while tweeting a random Quranic verse.\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        print(error_message)
