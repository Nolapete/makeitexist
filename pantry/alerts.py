from django.core.mail import send_mail
from django.conf import settings

from .models import Item


def send_alert(user, subject, message):
    if user.email:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
