# Generated by Django 5.0.2 on 2024-02-17 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "name",
                    models.CharField(
                        help_text="Name of the collection you want to access (e.g. 'Brainstorming' or 'London')",
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Collection Name",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                    "name",
                    models.CharField(
                        help_text="Your username",
                        max_length=255,
                        verbose_name="Username",
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ideahub.collection",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Idea",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, default="")),
                ("total_likes", models.IntegerField(default=0, editable=False)),
                ("total_dislikes", models.IntegerField(default=0, editable=False)),
                ("score", models.IntegerField(default=0, editable=False)),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ideahub.collection",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ideahub.user"
                    ),
                ),
            ],
            options={
                "unique_together": {("title", "collection")},
            },
        ),
        migrations.CreateModel(
            name="Vote",
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
                ("is_like", models.BooleanField(null=True)),
                (
                    "idea",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ideahub.idea"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ideahub.user"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="vote",
            constraint=models.UniqueConstraint(
                models.F("user"), models.F("idea"), name="vote_constraint"
            ),
        ),
    ]
