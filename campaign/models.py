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

        def representation(self):
                return {
                        'id': self.id,
                        'name': self.name,
                        'title': self.title,
                        'description': self.description,
                        'goal': self.goal,
                        'raised': self.raised,
                        'image': self.image,
                        'end_date': self.end_date,
                        'is_active': self.is_active,
                        'is_featured': self.is_featured,
                        'is_approved': self.is_approved,
                        'is_completed': self.is_completed,
                        'is_successful': self.is_successful,
                        'is_cancelled': self.is_cancelled,
                        'is_deleted': self.is_deleted,
                        'is_draft': self.is_draft,
                        'is_rejected': self.is_rejected,
                        'user_profile': self.user_profile,
                        'beneficiary_name': self.beneficiary_name,
                        'background_description': self.background_description,
                        'what_campaign_will_do': self.what_campaign_will_do,
                        'campaign_category': self.campaign_category,
                        'campain_category_name': self.campaign_category.name,
                        'created_at': self.created_at,
                        'updated_at': self.updated_at,

                }