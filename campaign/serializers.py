from rest_framework import serializers
from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
        class Meta:
                model = Campaign
                fields = '__all__'

        def create(self, validated_data):
                return Campaign.objects.create(**validated_data)

        def update(self, instance, validated_data):
                instance.name = validated_data.get('name', instance.name)
                instance.save()
                return instance

