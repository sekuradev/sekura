# Generated by Django 5.0.2 on 2024-03-11 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0002_alter_archive_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="archive",
            name="content",
            field=models.FileField(upload_to=""),
        ),
    ]
