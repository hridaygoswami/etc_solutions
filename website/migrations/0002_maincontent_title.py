# Generated by Django 4.2.13 on 2024-07-14 19:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="maincontent",
            name="title",
            field=models.TextField(default="Title"),
        ),
    ]
