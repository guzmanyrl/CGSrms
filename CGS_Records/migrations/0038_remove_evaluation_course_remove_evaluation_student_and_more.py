# Generated by Django 5.1.2 on 2024-12-08 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CGS_Records', '0037_course_evaluation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='course',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='student',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Evaluation',
        ),
    ]