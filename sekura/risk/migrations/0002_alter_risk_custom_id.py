# Generated by Django 5.0.2 on 2024-03-11 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("risk", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="risk",
            name="custom_id",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]