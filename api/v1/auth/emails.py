from django.core.mail import send_mail
from random import randint
from django.conf import settings
from home.models import CustomUser
from django.utils import timezone
from datetime import timedelta


def send_otp_via_email(email, user, subject, reset=True):
    otp = randint(1000, 9999)
    message = f"{otp} - is your OTP. Use it before expires!"

    from_email = settings.EMAIL_HOST

    send_mail(subject, message, from_email, [email])

    # user = CustomUser.objects.get(email=email)
    if reset:
        user.reset_otp = otp
    else:
        user.otp = otp
        
    user.otp_entry = timezone.now() + timedelta(minutes=5)
    user.save()