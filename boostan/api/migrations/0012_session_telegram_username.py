# Generated by Django 3.2.13 on 2022-07-11 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_session_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Telegram ID'),
        ),
    ]
