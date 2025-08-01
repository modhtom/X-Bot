# Islamic Twitter (Elon Mask X) Bot

## Overview
This project is a sophisticated Twitter bot designed to automatically tweet diverse Islamic content. It operates on a precise, timezone-aware schedule and is built with a robust, modular architecture for easy maintenance and expansion.

The bot features a centralized error handler that sends detailed email notifications, a "dry run" mode for safe testing, and dynamic content fetching from various APIs and web scrapers. The project's core logic is managed by the `schedule` library for reliability, with each task running in a separate thread to ensure non-blocking execution=.

The bot is live on Twitter: **[@*QuranicWisdom*](https://x.com/_QuranicWisdom_)**

-----

## Features

  * **Diverse Content**: Automatically tweets Quran verses, Hadith, prophetic stories, Names of Allah, inspirational quotes, daily challenges, reminders, and more.
  * **Dynamic Data**: Fetches content from live sources, including the `alquran.cloud` API, `hadith.gading.dev` API, and web scrapers for articles and stories from Islamweb.
  * **Precise Scheduling**: Uses a clean, human-readable schedule (e.g., "every day at 10:00 in Cairo") to post content at the right time.
  * **Robust Error Handling**: A centralized error handler captures any exception, logs it to the console, and sends a detailed email report with a full traceback.
  * **Stateful Modules**: Smart, class-based modules for Azkar and Friday tweets manage their own state, ensuring no repetition and reliable execution cycles.
  * **Safe Testing Mode**: A "dry run" mode can be enabled via an environment variable to test the entire application logic without sending any actual tweets.
  * **Advanced API Handling**: Automatically handles Twitter API rate limits and skips duplicate content.
  * **Image Support**: Tweets images from URLs and supports posting links to Image hosted on third-party platforms.

-----

## Setup & Installation

Follow these steps to get the bot running on your local machine.

### 1\. Clone the Repository

```bash
git clone https://github.com/modhtom/IslamicTwitterBot.git
cd IslamicTwitterBot
```

### 2\. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3\. Install Dependencies

The project's dependencies include Flask, tweepy, pytz, BeautifulSoup4, python-dotenv, and schedule. Install them all from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4\. Configure Environment Variables

Create a **`.env`** file in the root of your project. This file is essential for storing your secret credentials and configuration settings securely. Copy the following content into it and add your own credentials.

```env
# Twitter API Credentials
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_SECRET=your_access_secret

# Email Credentials for Error Notifications
# NOTE: If using Gmail with 2FA, you must create an "App Password".
EMAIL_SENDER=your_sending_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=your_receiving_email@gmail.com

# Testing Mode Configuration
# Set to True to prevent the bot from sending real tweets (prints to console instead).
# Set to False or remove the line to enable live tweeting.
DRY_RUN=True
```

-----

## Project Structure

The project is organized into a modular structure for clarity and scalability:

  * **`main.py`**: The main entry point. Initializes all clients and runs the master schedule loop.
  * **`content.py`**: A centralized file containing all static lists of text content (e.g., prayers, inspirations, challenges), making it easy to manage without touching the application logic.
  * **`Helpers/`**: A directory for all client and utility modules.
      * `TweetClient.py`: A robust class for all interactions with the Twitter API.
      * `Email.py`: Contains the `ErrorHandler` class for centralized error reporting.
      * `Stories.py`, `Blogs.py`, `Fatwas.py`: Individual web scrapers for fetching dynamic content.
      * `QuranData.py`, `Date.py`: Helpers for fetching data from various public APIs.
  * **Content Directories (`Quran/`, `Dua/`, etc.)**: Each directory contains the logic for a specific type of content, keeping concerns separated.

-----

## Usage

After completing the setup, run the bot from your terminal:

```bash
python main.py
```

The bot will initialize and start its schedule. You will see log messages in your console indicating which jobs are running or being tested in dry run mode.

### Tweeting Flow

The bot's schedule is managed by the `schedule` library in `main.py` for precision and readability.

  * **Frequent Tasks**: Every 1-4-6 minutes, the bot posts content from a rotating pool that includes Quran verses, Azkar, and Names of Allah.
  * **Twice Daily**: Every 12 hours, the bot tweets content like articles from blogs, selected Fatwas, and a Hadith from Sahih al-Bukhari.
  * **Daily Tasks**: At specific times each day (in the "Africa/Cairo" timezone), the bot posts unique content like Islamic inspirations, daily challenges, and calendar reminders.
  * **Special Friday Tasks**: On Fridays, the schedule is enhanced with reminders to read Surah Al-Kahf and frequent duas.

-----

## Testing

The bot includes a safe testing mode to verify its functionality without posting to Twitter.

To use it, set the `DRY_RUN` variable in your `.env` file to `True`:

```env
DRY_RUN=True
```

When you run the bot, all tweet content will be printed to your console instead of being sent to the API. This allows you to check formatting, content fetching, and scheduling logic safely.

-----

## Customization

  * **Tweet Content**: To change or add static content like inspirations or prayers, simply edit the corresponding list in **`content.py`**.
  * **Tweet Schedule**: To change when a tweet is posted, modify its job definition in **`main.py`**. The syntax is self-explanatory (e.g., `schedule.every(30).minutes.do(...)`).
  * **Scrapers**: To change the source of scraped content, modify the corresponding scraper module in the `Helpers/` directory.

-----

## Troubleshooting

1.  **Rate Limit Issues**: The bot automatically detects Twitter's rate limits and will wait for **15 minutes** before retrying the failed request.
2.  **Duplicate Tweets**: Duplicate content is automatically detected and skipped by the bot.
3.  **Email Sending Issues**: If using Gmail, ensure your account allows access from less secure apps or, preferably, generate an **"App Password"** if you have 2-Factor Authentication enabled.

-----

## Contributing

Contributions are welcome\! Please feel free to open an issue to report a bug or suggest a feature, or submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.