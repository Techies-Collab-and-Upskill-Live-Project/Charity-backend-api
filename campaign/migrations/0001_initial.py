# Generated by Django 5.0 on 2023-12-27 14:28

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("campaign_category", "0001_initial"),
        ("customauth", "0002_customuser_first_name_customuser_last_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("goal", models.IntegerField()),
                ("raised", models.IntegerField()),
                ("image", models.ImageField(upload_to="campaign_images/")),
                ("video", models.FileField(upload_to="campaign_videos/")),
                ("end_date", models.DateTimeField()),
                ("is_active", models.BooleanField(default=False)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_approved", models.BooleanField(default=False)),
                ("is_completed", models.BooleanField(default=False)),
                ("is_successful", models.BooleanField(default=False)),
                ("is_cancelled", models.BooleanField(default=False)),
                ("is_deleted", models.BooleanField(default=False)),
                ("is_draft", models.BooleanField(default=False)),
                ("is_rejected", models.BooleanField(default=False)),
                ("beneficiary_name", models.CharField(max_length=255)),
                ("background_description", models.TextField()),
                ("what_campaign_will_do", models.TextField()),
                (
                    "campaign_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="campaign_category.campaigncategory",
                    ),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customauth.userprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
