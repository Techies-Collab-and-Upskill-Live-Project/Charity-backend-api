from rest_framework import serializers
from .models import Campaign, CampaignDocument, CampaignImages
from utils import upload_pdf_and_get_url, upload_image_and_get_url


class CampaignDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignDocument
        fields = '__all__'

class CampaignImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignImages
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    campaign_category_name = serializers.CharField(source='campaign_category.name', read_only=True)
    user_profile_name = serializers.CharField(source='user_profile.name', read_only=True)
    documents = CampaignDocumentSerializer(many=True, required=False)
    images = CampaignImagesSerializer(many=True, required=False)


    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ['id', 'raised', 'donor_count']  # Fields that should not be modified directly by the serializer


    def create(self, validated_data):
        documents_data = validated_data.pop('documents', [])

        images_data = validated_data.pop('images', [])

        campaign = Campaign.objects.create(**validated_data)

        document_files = self.context.get('document_files', [])
        image_files = self.context.get('image_files', [])


        for document_data in document_files:
            # Upload each document and get the URL, then create a CampaignDocument instance
            document_url = upload_pdf_and_get_url(document_data, 'campaign_documents')
            try:
                CampaignDocument.objects.create(campaign=campaign, document_url=document_url)
            except Exception as e:
                print("Error: ", e)

        for image_data in image_files:
            # Upload each document and get the URL, then create a CampaignDocument instance
            image_url = upload_image_and_get_url(image_data, 'campaign_images')
            try:
                CampaignImages.objects.create(campaign=campaign, image=image_url)
            except Exception as e:
                print("Error: ", e)

        return campaign
