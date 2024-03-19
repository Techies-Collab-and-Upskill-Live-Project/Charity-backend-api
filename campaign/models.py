from typing import Any
from django.db import models
from core.models import BaseModel
# from cloudinary.models import CloudinaryField

class CampaignDocument(models.Model):
    campaign = models.ForeignKey('Campaign', related_name='documents', on_delete=models.CASCADE)
    document_url = models.URLField(max_length=1024, blank=True, null=True)

class CampaignImages(models.Model):
    campaign = models.ForeignKey('Campaign', related_name='images', on_delete=models.CASCADE)
    image = models.URLField(max_length=1024, blank=True, null=True, default='https://asset.cloudinary.com/dbn9ejpno/dcbb0fbcd596ecbbd4f91c9d47c7cdc7')

class Campaign(BaseModel):
        title = models.CharField(max_length=255)
        description = models.TextField()
        campaign_category = models.ForeignKey('campaign_category.CampaignCategory', on_delete=models.CASCADE)
        goal = models.IntegerField()
        currency = models.CharField(max_length=255)
        goals_obj = models.CharField(max_length=1000)
        raised = models.IntegerField(default=0)
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
        bank_name = models.CharField(max_length=255)
        account_name = models.CharField(max_length=255)
        account_number = models.CharField(max_length=255)
        


        def __str__(self):
                return self.title
        