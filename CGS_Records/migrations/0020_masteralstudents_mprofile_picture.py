# Generated by Django 5.1.2 on 2024-11-23 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CGS_Records', '0019_doctoralstudents_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='masteralstudents',
            name='mprofile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/masteral_profile_pictures/'),
        ),
    ]
