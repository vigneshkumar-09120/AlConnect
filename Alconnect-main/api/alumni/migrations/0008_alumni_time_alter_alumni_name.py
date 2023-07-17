# Generated by Django 4.1.6 on 2023-03-15 01:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0007_category_description_alter_higherstudies_degree_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumni',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='name',
            field=models.CharField(max_length=100, null=True, validators=[django.core.validators.RegexValidator('[+-/%@$^&*()!:;]', inverse_match=True)]),
        ),
    ]