from rest_framework import serializers
from .models import Donation  # Update with the correct import path for your Donation model

class DonationsSerializer(serializers.ModelSerializer):
    campaign_title = serializers.CharField(source='campaign.title', read_only=True)
    donor_name = serializers.CharField(source='donor_id.name', read_only=True)
    class Meta:
        model = Donation
        fields = ['campaign', 'amount', 'id', 'campaign_title', 'donor_name']
        read_only_fields = ['id']

    def validate(self, attrs):
        donation = Donation(**attrs)
        donation.clean()  # Use the model's clean method to apply custom validation
        return attrs

   