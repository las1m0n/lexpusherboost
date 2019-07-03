from django.core.mail import send_mail
from django.conf import settings


def send_email(to, subject, text):
    send_mail(
        subject,
        text,
        settings.EMAIL_HOST_USER,
        [to],
        fail_silently=False,
    )
