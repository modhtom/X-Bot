# Twitter(X) Bot

## Overview

This project is a Twitter bot designed to automatically tweet Islamic content and send emails when errors occur. It leverages threading for concurrent task execution and includes various tweet types, including Quran verses, Azkar, names of Allah, Hadith, blogs, and more. The bot uses Tweepy for interacting with Twitter and smtplib for sending error emails.

The bot is live on Twitter: [_QuranicWisdom_](https://x.com/_QuranicWisdom_)

## Features

- Tweets Islamic content periodically, such as Quran verses, Hadith, and Azkar.
- Posts special tweets on Fridays.
- Tweets with or without images.
- Sends an email notification if any errors occur.
- Includes rate-limiting handling and duplicate content checks.

## Requirements

### Software Dependencies

- Python 3.8+
- Required libraries:
  - `tweepy`
  - `pytz`
  - `dotenv`
  - `requests`
  - `Flask`
  - `BeautifulSoup4`

Install all dependencies with:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file with the following keys:

```env
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_SECRET=your_access_secret
```

### Email Configuration

Add your email credentials in the `send()` and `send_file()` functions:

```python
email_sender = "your_email@gmail.com"
email_password = "your_password"
email_receiver = "receiver_email@gmail.com"
```

## File Structure

- **main.py**: Core logic for tweeting and error handling.
- **TwitterBot class**:
  - Handles interaction with Twitter API.
  - Implements tweeting, thread tweeting, and image uploads.
- **Email Helper**: Responsible for sending emails and file attachments in case of errors.

## Usage

1. **Run the Bot:**
   ```bash
   python main.py
   ```
2. The bot runs indefinitely, posting tweets based on daily schedules and Fridays.

### Tweeting Flow

1. Tweets every 16 minutes, covering Quran, Azkar, and other content.
2. Additional tweets twice daily.
3. Posts daily tasks (Islamic inspirations, challenges, etc.).
4. Special Friday tweets include Salah and Dua reminders.
5. Sleeps for longer periods (3 hours) between iterations.

## Error Handling

- Captures all exceptions during tweeting and sends an email with the error details.
- Example email content:
  ```
  An error occurred during handle_daily_tweets execution:
  Error Type: Exception
  Error Message: Rate limit exceeded.
  Traceback: (stack trace here)
  ```

## Customization

- Modify tweet content by editing the respective modules (e.g., `Friday.py`, `Quran.py`).
- Update schedules by changing `TWEET_BREAK` and `TWEET_BREAK_LONG`.
- Replace email settings with your credentials for error notifications.

## Contribution Guidelines

Contributions to this project are welcome. Follow these steps to contribute:

1. **Fork the Repository:**

   - Click the "Fork" button on the project GitHub page.

2. **Clone Your Fork:**

   ```bash
   git clone https://github.com/modhtom/Twitter_Bot
   cd twitter-bot
   ```

3. **Create a New Branch:**

   ```bash
   git checkout -b feature-name
   ```

4. **Make Your Changes:**

   - Ensure your code adheres to Python coding standards.
   - Test your changes thoroughly.

5. **Commit Your Changes:**

   ```bash
   git add .
   git commit -m "Add a meaningful message about your changes"
   ```

6. **Push to Your Fork:**

   ```bash
   git push origin feature-name
   ```

7. **Submit a Pull Request:**
   - Go to the original repository on GitHub.
   - Click "Compare & Pull Request" to submit your changes.

## Deployment

- Recommended for deployment on hosting platforms like Render.
- Adjustments for Render:
  Replace API keys initialization block with commented-out code using secrets files.
  And uncomment live.keep_alive() in main.py to make the bot stay alive.

## Troubleshooting

1. **Rate Limit Issues:**
   - Bot pauses for 5 hours upon encountering rate limits.
2. **Duplicate Tweets:**
   - Duplicate content is skipped automatically.
3. **Email Sending Issues:**
   - Ensure your email account allows access to third-party applications (e.g., enable "Allow less secure apps").
