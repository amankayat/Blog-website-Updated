# Generated by Django 4.1 on 2023-03-11 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Login', '0002_userprofile_created_at_userprofile_is_verified_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='token',
        ),
    ]
