from rest_framework.viewsets import GenericViewSet
from core.exception_handlers import response_schemas
from .serializers import CampaignSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Campaign
from campaign_category.models import CampaignCategory
from drf_spectacular.utils import extend_schema
import uuid
from rest_framework.permissions import IsAuthenticated


class CampaignView(GenericViewSet):
        serializer_class = CampaignSerializer

        permission_classes = [IsAuthenticated]


        # View to create a new campaign using the campaign category ID
        @response_schemas(
            response_model=CampaignSerializer, code=201, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Create a new campaign')
        def create(self, request, campaign_category_id, *args, **kwargs):
                try:
                        try:
                                # Retrieve the campaign category or raise Http404 if not found
                                campaign_category = CampaignCategory.objects.get(id=campaign_category_id)
                        except CampaignCategory.DoesNotExist:
                                return Response(
                                        {'error': 'Campaign category does not exist.'},
                                        status=status.HTTP_404_NOT_FOUND
                                )

                        # Define mandatory fields
                        mandatory_fields = ['name', 'title', 'description', 'goal', 'end_date', 'image', 'beneficiary_name', 'background_description', 'what_campaign_will_do']

                        # Get the attributes from the request data
                        data = request.data
                        missing_fields = [field for field in mandatory_fields if field not in data or not data[field]]

                        if missing_fields:
                            error_message = f"Missing or empty fields: {', '.join(missing_fields)}"
                            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

                        # Get the attributes from the request data
                        name = data['name']
                        title = data['title']
                        description = data['description']
                        goal = data['goal']
                        raised = 0
                        image = data['image']
                        end_date = data['end_date']
                        beneficiary_name = data['beneficiary_name']
                        background_description = data['background_description']
                        what_campaign_will_do = data['what_campaign_will_do']



                        # Extract user ID from the access token in the header
                        user_id = request.user.id

                        # Create a new campaign
                        campaign = Campaign.objects.create(
                                name=name,
                                title=title,
                                description=description,
                                campaign_category=campaign_category,
                                goal=goal,
                                raised=raised,
                                image=image,
                                end_date=end_date,
                                beneficiary_name=beneficiary_name,
                                background_description=background_description,
                                what_campaign_will_do=what_campaign_will_do,
                                user_profile_id=user_id
                        )

                        campaign.save()

                        # Serialize the campaign
                        serializer = CampaignSerializer(campaign)

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
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)