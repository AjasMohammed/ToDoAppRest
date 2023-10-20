from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.core.mail import send_mail

from random import randint

from django.conf import settings

from django.utils import timezone

from datetime import timedelta



def image_path(instance, file_name):
    return f"profiles/{instance.email}/{file_name}"


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(_('email address'), unique=True)
    new_email = models.EmailField(_('email address'), null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to=image_path, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=4, null=True, blank=True)
    reset_otp = models.CharField(max_length=4, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    password_reset = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    objects = CustomUserManager()

    @property
    def generate_otp(self):
        otp = randint(1000, 9999)

        message = f"{otp} - is your OTP. OTP has a validity of 5 minutes, Use it before expires."
        from_email = settings.EMAIL_HOST
        subject = 'ToDoApp Email Verification'

        self.otp = otp
        if self.new_email == '' or self.new_email == None:
            send_mail(subject, message, from_email, [self.email])
        else:
            send_mail(subject, message, from_email, [self.new_email])

        self.otp_expiry = timezone.now() + timedelta(minutes=5)

        self.save()

        return self.otp

    
    def __str__(self) -> str:
        return self.email
    

class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.title