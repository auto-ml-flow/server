# Generated by Django 5.0.6 on 2024-05-15 16:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("experiment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="runmodel",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]