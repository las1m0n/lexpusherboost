from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER


def send_email(to, subject, text):
    send_mail(
        subject,
        text,
        EMAIL_HOST_USER,
        [to],
        fail_silently=False,
    )
