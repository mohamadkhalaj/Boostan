# Generated by Django 3.2.13 on 2022-07-10 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_student_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address'),
        ),
    ]
