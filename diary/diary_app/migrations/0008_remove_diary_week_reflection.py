# Generated by Django 5.2.1 on 2025-06-26 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary_app', '0007_alter_user_is_active_diary_diarysuccess_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diary',
            name='week_reflection',
        ),
    ]
