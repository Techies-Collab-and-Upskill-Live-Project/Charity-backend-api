from rest_framework import serializers
from .models import CampaignCategory
from campaign.serializers import CampaignSerializer
import random


class CampaignCategorySerializer(serializers.ModelSerializer):
        featured_campaign = serializers.SerializerMethodField()

        class Meta:
                model = CampaignCategory
                fields = '__all__'

        def create(self, validated_data):
                return CampaignCategory.objects.create(**validated_data)
        
        def get_featured_campaign(self, obj):
                # Fetching all campaigns related to the category 'obj'
                campaigns = obj.campaigns.all()  # Adjust 'campaigns' if your related name is different
                if campaigns.exists():
                    # Select one random campaign
                    return CampaignSerializer(random.choice(campaigns)).data
                return None 