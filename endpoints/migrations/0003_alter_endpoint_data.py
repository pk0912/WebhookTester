# Generated by Django 3.2.2 on 2021-05-08 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0002_alter_endpoint_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='data',
            field=models.JSONField(default=[]),
        ),
    ]
