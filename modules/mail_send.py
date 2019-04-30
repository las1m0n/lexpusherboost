import smtplib


FROM_ADDRESS = '@gmail.com'
LOGIN = ''
PASSWORD = ''
SMTP_SERVER = 'smtp.gmail.com:587'


def send(to, subject, text):
    msg = "\r\n".join([
        f"From: {FROM_ADDRESS}",
        f"To: {to}",
        f"Subject: {subject}",
        "",
        text
    ])

    server = smtplib.SMTP(SMTP_SERVER)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(FROM_ADDRESS, to, msg)
    server.quit()
