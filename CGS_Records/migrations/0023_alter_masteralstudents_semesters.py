# Generated by Django 5.1.2 on 2024-11-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CGS_Records', '0022_alter_doctoralstudents_student_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masteralstudents',
            name='semesters',
            field=models.CharField(blank=True, choices=[('1st', '1st Semester'), ('2nd', '2nd Semester'), ('3rd', 'Summer')], max_length=100),
        ),
    ]