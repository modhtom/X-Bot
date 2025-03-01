from email.message import EmailMessage
import ssl
import smtplib


# TODO: enter email address and password
def send(str):
    email_sender = ""
    email_password = ""

    email_receiver = ""

    subject = ""

    body = f"{str}"

    em = EmailMessage()
    em["From"] = email_sender
    em["TO"] = email_receiver
    em["subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def send_file(log_file_name, log_email_subject):
    with open(log_file_name, "r") as log_file:
        log_contents = log_file.read()

        # Create an email message
        email_sender = ""
        email_password = ""
        email_receiver = ""

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = log_email_subject
        em.set_content(log_contents)

        # Send the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)
