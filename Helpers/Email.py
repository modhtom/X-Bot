import os
import smtplib
import ssl
import traceback
from email.message import EmailMessage


class ErrorHandler:
    def __init__(self):
        self.email_sender = os.getenv("EMAIL_SENDER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_receiver = os.getenv("EMAIL_RECEIVER")

    def _send_email(self, subject, body):
        if not all([self.email_sender, self.email_password, self.email_receiver]):
            print("ERROR: Email credentials not set in environment. Cannot send email.")
            return

        em = EmailMessage()
        em["From"] = self.email_sender
        em["To"] = self.email_receiver
        em["Subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.send_message(em)
                print(f"Email notification '{subject}' sent successfully.")
        except Exception as e:
            print(f"FATAL: Could not send email. Error: {e}")

    def handle_error(
        self, e: Exception, context_message: str = "An unspecified error occurred"
    ):
        error_report = (
            f"An error occurred in your Twitter Bot.\n"
            f"Context: {context_message}\n\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n\n"
            f"Traceback:\n{traceback.format_exc()}"
        )

        print("--- ERROR REPORT ---")
        print(error_report)
        print("--------------------")

        self._send_email(f"Twitter Bot Error: {type(e).__name__}", error_report)
