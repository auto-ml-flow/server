# Generated by Django 5.0.6 on 2024-05-19 21:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PreparedDatasetModel",
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
                ("labels", models.JSONField()),
                ("target", models.CharField(max_length=100)),
                ("csv_file", models.FileField(upload_to="prepared_datasets")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MetaAlgoModel",
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
                (
                    "type",
                    models.CharField(
                        choices=[("DURATION", "DURATION"), ("PREDICT", "PREDICT")],
                        default="DURATION",
                        max_length=8,
                    ),
                ),
                ("model", models.FileField(upload_to="meta_algos")),
                ("mse", models.FloatField()),
                ("rmse", models.FloatField()),
                ("max_error", models.FloatField()),
                ("min_error", models.FloatField()),
                (
                    "dataset",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="models",
                        to="meta_algo.prepareddatasetmodel",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
