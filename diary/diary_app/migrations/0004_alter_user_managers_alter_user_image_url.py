# Generated by Django 5.2.1 on 2025-06-01 07:55

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary_app', '0003_rename_expired_useractivatetoken_expired_at'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='image_url',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
