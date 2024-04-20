# Generated by Django 5.0.4 on 2024-04-19 23:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_disk_region_band_molecule_disk_region"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="molecule",
            name="file",
        ),
        migrations.CreateModel(
            name="Data",
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
                ("name", models.CharField(max_length=40)),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("data", models.FileField(upload_to="data/")),
                ("is_viewable", models.BooleanField(default=False)),
                (
                    "molecule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.molecule"
                    ),
                ),
            ],
        ),
    ]
