# Generated by Django 5.0 on 2023-12-27 01:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customauth", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
