# Generated by Django 4.2.13 on 2024-07-17 14:53

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_maincontent_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="image",
            field=models.ImageField(upload_to=website.models.upload_to),
        ),
    ]
