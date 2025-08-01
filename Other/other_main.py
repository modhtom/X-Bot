import random
from Helpers import (
    Stories,
    Fatwas as fatwa,
    TweetClient,
    Blogs as blog,
    Date as date,
    Email,
    content,
)
from datetime import datetime, timedelta

error_handler = Email.ErrorHandler()


def tweet_islamic_calendar_reminders(bot: TweetClient.TwitterBot):
    islamic_date = date.get_islamic_date()
    if islamic_date in content.islamic_events:
        try:
            event_message = content.islamic_events[islamic_date]
            tweet = (
                f"🗓️ حدث اليوم:\n{event_message}\n\n"
                f"🌙 لا تنسوا إحياء هذا اليوم بالذكر والعمل الصالح.\n"
                f"#التقويم_الإسلامي #إيمان"
            )
            bot.tweet(tweet)
        except Exception as e:
            error_handler.handle_error(f"error {e}")

    # Check if tomorrow is Monday or Thursday
    tomorrow = datetime.now() + timedelta(days=1)
    if tomorrow.weekday() == 0 or tomorrow.weekday() == 3:  # Monday = 0, Thursday = 3
        try:
            reminder_message = (
                f"🌟 تذكير:\nغداً هو {'الإثنين' if tomorrow.weekday() == 0 else 'الخميس'}، "
                f"وهو من الأيام المحبب فيها الصيام اقتداءً بسنة النبي محمد ﷺ.\n\n"
                f"💡 اغتنموا هذا الأجر العظيم 🌙.\n#صيام_سنة #إيمان"
            )
            bot.tweet(reminder_message)
        except Exception as e:
            error_handler.handle_error(f"Error while tweeting fasting reminder: {e}")


def tweet_prophetic_stories(bot: TweetClient.TwitterBot):
    base_url = "https://www.islamweb.net/ar/articles/138/السيرة-النبوية"
    page_number = random.randint(1, 64)
    stories_url = f"{base_url}?pageno={page_number}"

    try:
        story_links = Stories.story_scraper(stories_url)
        if not story_links:
            print("No prophetic stories found to tweet.")
            return

        title, url = random.choice(story_links)
        print(f"Fetching content for story: {title}")
        summary = Stories.get_story_content(url)
        if not summary:
            print(f"Could not extract summary for {title}")
            return

        tweet = (
            f"📜 قصة من السيرة-النبوية: {title}\n\n"
            f"💬 {summary}\n\n"
            f"🔗 لقراءة القصة كاملة: {url}\n\n"
            f"✨ #السيرة-النبوية# عبرة"
        )
        bot.tweet(tweet)

    except Exception as e:
        error_handler.handle_error(e, "Failed to scrape or tweet a prophetic story.")


def tweet_names_of_allah(bot: TweetClient.TwitterBot):

    name_info = random.choice(content.names_and_meanings)
    tweet_text = (
        f"✨ اسم الله: {name_info['name']}\n\n"
        f"📖 معناه: {name_info['meaning']}\n"
        f"📌 شاركنا اسم الله الذي تحبه أكثر 🤍.\n"
        f"#أسماء_الله_الحسنى #ذكر"
    )

    try:
        bot.tweet(tweet_text)
    except Exception as e:
        error_handler.handle_error(f"error: {e}")


def tweet_islamic_inspirations(bot: TweetClient.TwitterBot):

    inspiration = random.choice(content.inspirations)
    try:
        bot.tweet(
            f"💡 {inspiration}\n\n"
            f"🤲 اذكر الله واستلهم منه السكينة.\n"
            f"#إلهام_إسلامي #ذكر_الله"
        )
    except Exception as e:
        error_handler.handle_error(f"Error tweeting Islamic inspiration: {e}")


def tweet_islamic_challenges(bot: TweetClient.TwitterBot):
    challenge = random.choice(content.challenges)
    try:
        bot.tweet(
            f"🕌 تحدي اليوم:\n{challenge}\n\n"
            f"📌 جرب هذه الخطوة الصغيرة لتحسين نفسك.\n"
            f"#تحدي_يومي #إسلام"
        )
    except Exception as e:
        error_handler.handle_error(f"Error tweeting Islamic challenge: {e}")


tweeted_blogs = set()
tweeted_fatwas = set()


def tweet_content(
    bot: TweetClient.TwitterBot,
    articles,
    tweeted_items,
    get_content,
    clean_content,
    tweet_format,
    max_tweets=1,
):
    tweets_sent = 0
    for title, article_url in articles:
        if tweets_sent >= max_tweets:
            break

        if article_url in tweeted_items:
            error_handler.handle_error(f"Already tweeted: {article_url}")
            continue

        content_data = get_content(article_url)
        if content_data is None:
            error_handler.handle_error(f"Could not retrieve content for {article_url}")
            continue

        cleaned_data = clean_content(content_data[0])
        tweet_text = tweet_format(title, cleaned_data, article_url)
        bot.tweet(tweet_text)
        tweeted_items.add(article_url)

        tweets_sent += 1


def fetch_and_tweet(
    url_format,
    max_pages,
    scrape_articles,
    tweeted_items,
    get_content,
    clean_content,
    tweet_format,
    max_tweets=1,
):
    try:
        for page_number in range(1, max_pages + 1):
            url = url_format.format(page_number=page_number)
            articles = scrape_articles(url)
            if not articles:
                error_handler.handle_error("No articles found.")
                return
            tweet_content(
                articles,
                tweeted_items,
                get_content,
                clean_content,
                tweet_format,
                max_tweets,
            )
            if len(tweeted_items) >= max_tweets:
                break
    except Exception as e:
        error_message = (
            f"An error occurred:\n"
            f"Last page number: {page_number}\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
        )
        error_handler.handle_error(error_message)


def extract_key_points(content, max_length=250):
    paragraphs = content.split("\n\n")
    meaningful_paragraphs = [p for p in paragraphs if len(p) > 50]

    if meaningful_paragraphs:
        main_content = meaningful_paragraphs[0]
        if len(main_content) > max_length:
            last_period = main_content[:max_length].rfind(".")
            if last_period > max_length * 0.7:
                main_content = main_content[: last_period + 1]
            else:
                main_content = main_content[:max_length] + "..."

        return main_content
    return content[:max_length] + "..."


def extract_teaser(content, max_length=150):
    if not content or len(content) < 5:
        return "اقرأ المزيد للإجابة التفصيلية..."

    paragraphs = content.split("\n\n")
    meaningful_paragraphs = [p for p in paragraphs if len(p) > 20]

    if not meaningful_paragraphs:
        return content[:max_length] + "..."

    for paragraph in meaningful_paragraphs[:2]:
        sentences = paragraph.split(". ")
        for sentence in sentences:
            if "?" in sentence and len(sentence) < max_length:
                return sentence + "..."

    main_content = meaningful_paragraphs[0]

    if len(main_content) > max_length:
        cutoff_point = main_content[:max_length].rfind("،")
        if cutoff_point == -1 or cutoff_point < max_length * 0.5:
            cutoff_point = main_content[:max_length].rfind(" ")

        return main_content[:cutoff_point] + "..."

    return main_content


def get_key_themes(content, count=3):
    if not content or len(content) < 20:
        return ["الفتوى", "حكم_شرعي", "استشارة"]

    found_themes = []
    for theme in content.common_islamic_themes:
        if theme in content and len(found_themes) < count:
            found_themes.append(theme)

    if len(found_themes) < count:
        default_themes = ["الفتوى", "حكم_شرعي", "استشارة"]
        for theme in default_themes:
            if theme not in found_themes and len(found_themes) < count:
                found_themes.append(theme)

    return found_themes


def extract_fatwa_topics(title):
    topics = []

    for topic, keywords in content.topic_keywords.items():
        for keyword in keywords:
            if keyword in title and topic not in topics:
                topics.append(topic)
                break

    if not topics:
        if "زوج" in title or "طلاق" in title:
            return ["الأحوال_الشخصية", "الأسرة", "الاستشارات"]
        return ["الفتوى", "حكم_شرعي", "استشارة"]

    return topics[:3]


def tweet_blogs():
    url_format = (
        "https://www.islamweb.net/ar/articles/46/أخلاق-وتزكية?pageno={page_number}"
    )
    max_pages = 45
    fetch_and_tweet(
        url_format,
        max_pages,
        blog.scrape_articles,
        tweeted_blogs,
        blog.get_blog_content,
        blog.clean_content,
        lambda title, content, url: (
            f"📝 {title}\n\n"
            f"💎 قيم المقال: {' | '.join(['#' + theme for theme in get_key_themes(content)])}\n\n"
            f"هل تريد معرفة الحكمة الكاملة؟ 👇\n"
            f"📖 لقراءة المزيد: {url}\n\n"
            f"🔄 شارك المقال مع من تحب وساهم في نشر العلم 🌟\n"
            f"#أخلاق #تزكية #إسلام"
        ),
        max_tweets=1,
    )


def tweet_fatwas():
    url_format = "https://www.islamweb.net/ar/fatwa/مختارات-الفتوى?pageno={page_number}"
    max_pages = 259
    fetch_and_tweet(
        url_format,
        max_pages,
        fatwa.scrape_articles,
        tweeted_fatwas,
        fatwa.get_fatwa_content,
        lambda data: {
            "question": (
                data[0]
                if data[0] and len(data[0]) > 5
                else f"سؤال حول {data[0] or 'حكم شرعي'} (اضغط للتفاصيل)"
            ),
            "answer": (
                data[1]
                if data[1] and len(data[1]) > 5
                else "اقرأ الفتوى كاملة للاطلاع على الإجابة التفصيلية من علماء موثوقين..."
            ),
            "themes": extract_fatwa_topics(data[0] if len(data[0]) > 5 else ""),
        },
        lambda title, content, url: (
            f"📝 {title}\n\n"
            f"📊 موضوعات الفتوى: {' | '.join(['#' + theme for theme in content['themes']])}\n\n"
            f"🤔 تريد معرفة الحكم الشرعي كاملاً؟\n"
            f"🔗 اقرأ الفتوى: {url}\n\n"
            f"🔄 شارك الفتوى مع من تحب لتعم الفائدة 🌟\n"
            f"#فتاوى #إسلام #علم"
        ),
        max_tweets=1,
    )
