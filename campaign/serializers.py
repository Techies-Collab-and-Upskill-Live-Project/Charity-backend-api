from rest_framework import serializers
from .models import Campaign
import cloudinary
from campaign_category.models import CampaignCategory

class CampaignSerializer(serializers.Serializer):
    name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    goal = serializers.DecimalField(max_digits=10, decimal_places=2)
    end_date = serializers.DateTimeField()
    image = serializers.ImageField()
    beneficiary_name = serializers.CharField()
    background_description = serializers.CharField()
    what_campaign_will_do = serializers.CharField()

    def create(self, validated_data):
        campaign_category_id = self.context.get('campaign_category_id')
        campaign_category = CampaignCategory.objects.filter(id=campaign_category_id).first()
        if not campaign_category:
            raise serializers.ValidationError({'error': 'Campaign category does not exist.'})

        user_id = self.context.get('user_id')

        campaign = Campaign.objects.create(
            campaign_category=campaign_category,
            raised=0,
            user_profile_id=user_id,
            **validated_data
        )

        image = validated_data.get('image')
        if image:
            try:
                print("before upload")
                uploaded_image = cloudinary.uploader.upload(image, folder='campaign_images')
                campaign.image = uploaded_image['url']
            except Exception as upload_error:
                raise serializers.ValidationError({'error': f'Image upload error: {str(upload_error)}'})

        campaign.save()
        return campaign

#   def to_representation(self, instance):
#              representation = super().to_representation(instance)
#              representation['image'] = instance.image
#              return representation
#    def update(self, instance, validated_data):
#              image = validated_data.get('image')
#              if image:
#                      image = cloudinary.uploader.upload(image)
#                      instance.image = image['url']
#              instance.save()
#              return instance
