import smtplib
from email.mime.text import MIMEText


def send_email(user_email: str, user_weight: str, average_weight: float or int, total_queries) -> None:
    from_email = "youremailgoeshere@youremail.com"
    from_password = "your_password"  # We determine the sender's email.
    to_email = user_email
    subject = "Weight data and information"
    message = "Hey there, your weight is <strong>%s</strong>. The average is <strong>%s</strong> out of an average of " \
              "<strong>%s</strong> people." % (
                  user_weight, average_weight, total_queries)  # We E-Mail the user information.

    msg = MIMEText(message, "html")  # We generate the email...
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)  # And off it goes! Working perfectly.
