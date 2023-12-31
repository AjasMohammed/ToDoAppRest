# Generated by Django 4.2.6 on 2023-10-19 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_task_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/'),
        ),
    ]
