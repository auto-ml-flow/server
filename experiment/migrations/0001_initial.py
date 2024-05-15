# Generated by Django 5.0.6 on 2024-05-15 16:41

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExperimentModel",
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
                ("name", models.CharField(max_length=500, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RunModel",
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
                ("duration", models.FloatField(blank=True, default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CREATED", "CREATED"),
                            ("STARTED", "STARTED"),
                            ("FAILED", "FAILED"),
                            ("DONE", "DONE"),
                        ],
                        default="CREATED",
                        max_length=7,
                    ),
                ),
                ("traceback", models.TextField(blank=True, null=True)),
                (
                    "experiment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="runs",
                        to="experiment.experimentmodel",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="RunMetricModel",
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
                ("key", models.CharField(max_length=100)),
                ("value", models.FloatField()),
                (
                    "run",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="metrics",
                        to="experiment.runmodel",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
