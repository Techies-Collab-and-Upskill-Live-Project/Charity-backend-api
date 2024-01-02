from django.db import models
from core.models import BaseModel

class CampaignCategory(BaseModel):
        name = models.CharField(max_length=255, unique=True, error_messages={'unique': 'This campaign category name already exists'})
        description = models.TextField()

        def __str__(self):
                return self.name


