# Generated by Django 4.2.6 on 2023-10-19 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_customuser_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='new_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address'),
        ),
    ]