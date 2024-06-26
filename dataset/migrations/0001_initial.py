# Generated by Django 5.0.6 on 2024-05-18 16:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("experiment", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DatasetModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="creation date"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="last update date",
                    ),
                ),
                ("n_samples", models.IntegerField()),
                ("n_features", models.IntegerField()),
                ("file", models.FileField(upload_to="datasets")),
                (
                    "run",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dataset",
                        to="experiment.runmodel",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
