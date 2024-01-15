from typing import Any
from django.db import models
from core.models import BaseModel


class Campaign(BaseModel):
        name = models.CharField(max_length=255)
        title = models.CharField(max_length=255)
        description = models.TextField()
        campaign_category = models.ForeignKey('campaign_category.CampaignCategory', on_delete=models.CASCADE)
        goal = models.IntegerField()
        raised = models.IntegerField()
        image = models.ImageField(upload_to='campaign_images/')
        end_date = models.DateTimeField()
        donor_count = models.IntegerField(default=0)
        is_active = models.BooleanField(default=False)
        is_featured = models.BooleanField(default=False)
        is_approved = models.BooleanField(default=False)
        is_completed = models.BooleanField(default=False)
        is_successful = models.BooleanField(default=False)
        is_cancelled = models.BooleanField(default=False)
        is_deleted = models.BooleanField(default=False)
        is_draft = models.BooleanField(default=False)
        is_rejected = models.BooleanField(default=False)
        user_profile = models.ForeignKey('customauth.UserProfile', on_delete=models.CASCADE)
        beneficiary_name = models.CharField(max_length=255)
        background_description = models.TextField()
        what_campaign_will_do = models.TextField()


        def __str__(self):
                return self.name
