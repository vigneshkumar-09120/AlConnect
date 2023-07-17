# Generated by Django 4.1.6 on 2023-02-07 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_rename_student_skills_stud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skills',
            name='stud',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='student.student'),
        ),
    ]
