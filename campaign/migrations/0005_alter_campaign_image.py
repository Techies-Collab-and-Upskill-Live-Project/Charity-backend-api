# Generated by Django 5.0.2 on 2024-03-12 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaign", "0004_alter_campaign_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="image",
            field=models.URLField(
                blank=True,
                default="https://asset.cloudinary.com/dbn9ejpno/dcbb0fbcd596ecbbd4f91c9d47c7cdc7",
                null=True,
            ),
        ),
    ]
