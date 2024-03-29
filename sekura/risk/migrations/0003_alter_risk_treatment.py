# Generated by Django 5.0.2 on 2024-03-11 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("risk", "0002_alter_risk_custom_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="risk",
            name="treatment",
            field=models.CharField(
                blank=True,
                choices=[("M", "Mitigate"), ("T", "Transfer"), ("A", "Avoid"), ("C", "Accept"), (None, "Not set")],
                max_length=3,
                null=True,
            ),
        ),
    ]
