# Generated by Django 5.1.2 on 2024-11-27 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CGS_Records', '0031_alter_doctoralstudents_student_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoralstudents',
            name='programs',
            field=models.CharField(blank=True, choices=[('PhD. Ed. EM', 'PhD. Ed'), ('PhD. TM', 'PhD. TM'), ('DM', 'DM')], max_length=50),
        ),
    ]
