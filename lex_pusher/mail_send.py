from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER


def send_email():
    send_mail(
        'Subject here',
        'Here is the message.',
        EMAIL_HOST_USER,
        ['svinerus@gmail.com'],
        fail_silently=False,
    )
