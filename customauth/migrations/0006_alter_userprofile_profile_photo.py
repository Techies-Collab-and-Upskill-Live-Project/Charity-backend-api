# Generated by Django 5.0.2 on 2024-04-09 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customauth", "0005_customuser_registration_method"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_photo",
            field=models.URLField(blank=True),
        ),
    ]