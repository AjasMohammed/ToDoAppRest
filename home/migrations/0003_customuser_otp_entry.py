# Generated by Django 4.2.6 on 2023-10-18 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_customuser_is_verified_customuser_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp_entry',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
