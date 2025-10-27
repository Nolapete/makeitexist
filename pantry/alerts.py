from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Stock, Item
from django.utils import timezone


def send_alert(user, subject, message):
    if user.email:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
