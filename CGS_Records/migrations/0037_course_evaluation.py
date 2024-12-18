# Generated by Django 5.1.2 on 2024-12-08 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CGS_Records', '0036_delete_evaluationofgrades'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_no', models.CharField(max_length=10)),
                ('course_name', models.CharField(max_length=100)),
                ('units', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('units_earned', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='CGS_Records.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='CGS_Records.doctoralstudents')),
            ],
        ),
    ]
