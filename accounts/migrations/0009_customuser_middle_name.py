# Generated by Django 5.1.2 on 2024-11-22 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customuser_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(default=2, max_length=30),
            preserve_default=False,
        ),
    ]
