from rest_framework import serializers
from .models import CampaignCategory

class CampaignCategorySerializer(serializers.ModelSerializer):
        class Meta:
                model = CampaignCategory
                fields = '__all__'

        def create(self, validated_data):
                return CampaignCategory.objects.create(**validated_data)