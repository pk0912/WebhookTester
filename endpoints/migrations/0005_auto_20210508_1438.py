# Generated by Django 3.2.2 on 2021-05-08 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("endpoints", "0004_alter_endpoint_data"),
    ]

    operations = [
        migrations.RemoveField(model_name="endpoint", name="data",),
        migrations.CreateModel(
            name="EndpointHits",
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
                ("query_params", models.JSONField(default=list)),
                ("raw_body", models.JSONField(default=dict)),
                ("headers", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="endpoints.endpoint",
                    ),
                ),
            ],
        ),
    ]
