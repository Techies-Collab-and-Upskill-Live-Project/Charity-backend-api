from rest_framework.viewsets import GenericViewSet
from core.exception_handlers import response_schemas
from .serializers import CampaignSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Campaign
from campaign_category.models import CampaignCategory
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary
from utils import upload_image_and_get_url



class CampaignView(GenericViewSet):
        serializer_class = CampaignSerializer

        permission_classes = [IsAuthenticated]
        parser_classes = (MultiPartParser, FormParser)

        # View to create a new campaign using the campaign category ID

        @response_schemas(
            response_model=CampaignSerializer, code=201, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Create a new campaign')
        def create(self, request, campaign_category_id, *args, **kwargs):
                try:
                        data = request.data.copy()
                        data['campaign_category'] = campaign_category_id
                        data['user_profile'] = request.user.id
                        # # Handle image separately if it's part of the data
                        # if 'image' in data:
                        #         data['image'] = upload_image_and_get_url(data['image'], 'campaign_images')
                        
                        # Handle document files
                        document_files = request.FILES.getlist('documents')  
                        image_files = request.FILES.getlist('images')
                        serializer = CampaignSerializer(data=data, context={'request': request, 'document_files': document_files, 'image_files': image_files})


                        serializer.is_valid(raise_exception=True)
                        campaign = serializer.save()
                        campaign.save
                        
                        # Serialize the campaign
                        response_data = {
                            'campaign': serializer.data,
                            'message': 'Campaign created successfully'
                        }
                        return Response(response_data, status=status.HTTP_201_CREATED)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # View to get all campaigns
        @response_schemas(
            response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Get all campaigns')
        def list(self, request, *args, **kwargs):
                try:
                        campaigns = Campaign.objects.all()
                        serializer = CampaignSerializer(campaigns, many=True)
                        # Calculate the count of campaigns
                        count = len(campaigns)

                        # Create a dictionary including both the serialized data and the count
                        response_data = {
                            "campaigns": serializer.data,
                            "count": count,
                            "message": "All campaigns retrieved successfully"
                        }

                        return Response(response_data, status=status.HTTP_200_OK)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # View to get all campaigns by category
        @response_schemas(
                response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Get all campaigns by category')
        def list_by_category(self, request, campaign_category_id, *args, **kwargs):
                try:
                        # Retrieve the campaign category or raise Http404 if not found
                        campaign_category = CampaignCategory.objects.get(id=campaign_category_id)

                        # Retrieve all campaigns by category
                        campaigns = Campaign.objects.filter(campaign_category=campaign_category)
                        serializer = CampaignSerializer(campaigns, many=True)

                        # Calculate the count of campaigns
                        count = len(campaigns)

                        # Create a dictionary including both the serialized data and the count
                        response_data = {
                                f"campaigns in {campaign_category.name} ": serializer.data,
                                "count": count,
                                "message": f"All campaigns in {campaign_category.name} category retrieved successfully"
                        }

                        return Response(response_data, status=status.HTTP_200_OK)
                except CampaignCategory.DoesNotExist:
                        return Response(
                                {'error': 'Campaign category does not exist.'},
                                status=status.HTTP_404_NOT_FOUND
                        )


        # View to get a single campaign
        @response_schemas(
            response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Get a single campaign')
        def retrieve(self, request, campaign_id, *args, **kwargs):
                try:

                        campaign = Campaign.objects.get(id=campaign_id)
                        serializer = CampaignSerializer(campaign)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Campaign.DoesNotExist:
                        return Response({"message": "Campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # View to update a single campaign
        @response_schemas(
            response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Update a single campaign')
        def update(self, request, campaign_id, *args, **kwargs):
                try:
                        campaign = Campaign.objects.get(id=campaign_id)
                        serializer = CampaignSerializer(campaign, data=request.data)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Campaign.DoesNotExist:
                        return Response({"message": "Campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # View to delete a single campaign
        @response_schemas(
            response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Delete a single campaign')
        def destroy(self, request, campaign_id, *args, **kwargs):
                try:
                        campaign = Campaign.objects.get(id=campaign_id)
                        campaign.delete()
                        return Response({"message": "Campaign deleted successfully"}, status=status.HTTP_200_OK)
                except Campaign.DoesNotExist:
                        return Response({"message": "Campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                        return Response(
                                {
                                        "message": str(e)
                                },
                                status=status.HTTP_400_BAD_REQUEST)
                
        
        # View to delete all campaigns
        @response_schemas(
            response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Delete all campaign')
        def destroy_all(self, request, *args, **kwargs):
                try:
                        Campaign.objects.all().delete()
                        return Response({"message": "All campaigns deleted successfully"}, status=status.HTTP_200_OK)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)