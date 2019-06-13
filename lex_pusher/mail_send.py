import smtplib


FROM_ADDRESS = 'bondarenkonikita295@gmail.com'
LOGIN = "bondarenkonikita295@gmail.com"
PASSWORD = "7325462896nk"


def send(to, subject, text):
    msg = "\r\n".join([
        f"From: {FROM_ADDRESS}",
        f"To: {to}",
        f"Subject: {subject}",
        "",
        text
    ])

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(FROM_ADDRESS, to, msg)
    server.quit()



