# Generated by Django 5.1.2 on 2024-12-18 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CGS_Records', '0038_remove_evaluation_course_remove_evaluation_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masteralstudents',
            name='student_type',
            field=models.CharField(blank=True, choices=[('new', 'new'), ('Old', 'Old')], max_length=100),
        ),
    ]
