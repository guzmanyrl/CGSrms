# Generated by Django 5.1.1 on 2024-10-25 05:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_otp_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.EmailField(default=django.utils.timezone.now, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.EmailField(default=django.utils.timezone.now, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]