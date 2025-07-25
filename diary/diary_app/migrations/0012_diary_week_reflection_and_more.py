# Generated by Django 5.2.1 on 2025-07-05 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary_app', '0011_alter_user_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='week_reflection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='diary_app.weekreflection'),
        ),
        migrations.AlterField(
            model_name='weekreflection',
            name='month_reflection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diary_app.monthreflection'),
        ),
    ]
