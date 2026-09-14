import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.config import GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL

def send_newsletter(html_body, subject="Your Daily AI/Tech Digest"):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT_EMAIL

    # Plain text fallback
    text_part = MIMEText("Your newsletter is ready. View this email in HTML mode.", "plain")
    html_part = MIMEText(html_body, "html")

    msg.attach(text_part)
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        print(f"[mail sent] to {RECIPIENT_EMAIL}")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"[mail fail] Auth error: {e}. Check App Password.")
        return False
    except smtplib.SMTPException as e:
        print(f"[mail fail] SMTP error: {e}")
        return False
    except Exception as e:
        print(f"[mail fail] {type(e).__name__}: {e}")
        return False