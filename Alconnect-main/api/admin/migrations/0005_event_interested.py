# Generated by Django 4.1.6 on 2023-03-30 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0004_event_time_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='interested',
            field=models.IntegerField(null=True),
        ),
    ]
