from django.db import models
from django.core.exceptions import ValidationError
from campaign.models import Campaign
from django.contrib.auth import get_user_model
from core.models import BaseModel

User = get_user_model()

class Donation(BaseModel):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # donor name should be linked to the user profile
    donor_id = models.ForeignKey('customauth.UserProfile', on_delete=models.CASCADE)

    def clean(self):
        # Ensure the campaign is active
        if not self.campaign.is_active:
            raise ValidationError("Campaign not active")
        # Ensure the campaign is not completed
        if self.campaign.is_completed:
            raise ValidationError("Cannot donate to a completed campaign.")

        # Check if the donation amount exceeds the campaign's remaining goal
        remaining_goal = self.campaign.goal - self.campaign.raised
        if self.amount > remaining_goal:
            raise ValidationError("Donation amount exceeds the campaign's remaining goal.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
        self.campaign.raised += self.amount
        self.campaign.donor_count += 1  # Increment the donor count
        self.campaign.save()
        # super().save(*args, **kwargs)
