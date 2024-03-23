from rest_framework.viewsets import GenericViewSet
from core.exception_handlers import response_schemas
from core.permissions import IsAdminUser
from .serializers import CampaignSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import F, Q
from datetime import timedelta
from .models import Campaign
from campaign_category.models import CampaignCategory
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
import random




class CampaignView(GenericViewSet):
        serializer_class = CampaignSerializer

        # permission_classes = [IsAuthenticated]
        parser_classes = (MultiPartParser, FormParser)
        def get_permissions(self):
            """
            Instantiates and returns the list of permissions that this view requires.
            """
            # For example, if you want the 'destroy_all' method to require the user to be an admin
            if self.action in ['destroy_all', 'approve']:
                permission_classes = [IsAdminUser]
            elif self.action in ['create', 'update', 'destroy']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = []
                
            return [permission() for permission in permission_classes]
        
        # View to create a new campaign using the campaign category ID

        @response_schemas(
            response_model=CampaignSerializer, code=201, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Create a new campaign')
        def create(self, request, campaign_category_id, *args, **kwargs):
                try:
                        data = request.data.copy()
                        # check if campaign category exists
                        campaign_category = CampaignCategory.objects.get(id=campaign_category_id)
                        if not campaign_category:
                                return Response({"message": "Campaign category not found"}, status=status.HTTP_404_NOT_FOUND)
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
                
        
        # View to get trending campaigns
        @response_schemas(
            response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Get trending campaigns')
        def trending(self, request, *args, **kwargs):
                try:
                     # Get the current date and time
                     now = timezone.now()
             
                     # Define a recent timeframe, e.g., campaigns that received donations in the last 7 days
                     recent_days = 7
                     recent_threshold = now - timedelta(days=recent_days)
                     print("recent_threshold: ", recent_threshold)
             
                     # Filter for active campaigns that are not completed, cancelled, deleted, or rejected, and have an end date in the future
                     campaigns = Campaign.objects.filter(
                         is_active=True,
                         is_completed=False,
                         is_cancelled=False,
                         is_deleted=False,
                         is_rejected=False,
                         end_date__gte=now,
                     )

                     # Further filter for campaigns that have recent activity
                     # This requires a way to track when donations are made, which may require adjustments to your model
                     # For this example, we'll assume 'raised' and 'donor_count' can reflect recent activity
                     campaigns = campaigns.annotate(
                         recent_activity=F('raised') + F('donor_count')
                     ).filter(
                         recent_activity__gt=0,  # Adjust this condition based on your data
                         date_updated__gte=recent_threshold
                     )
             
                     # Order the campaigns by 'recent_activity' and then by the total amount raised
                     trending_campaigns = campaigns.order_by('-recent_activity', '-raised')[:3]  # Get the top 3 trending campaigns
             
                     # Serialize and return the trending campaigns
                     serializer = CampaignSerializer(trending_campaigns, many=True)
                     response = {
                         "message": "Trending campaigns retrieved successfully",
                         "data": serializer.data,
                         "count": len(trending_campaigns)
                     }
                     return Response(response, status=status.HTTP_200_OK)
                       
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        
        # View to approve a campaign
        @response_schemas(
            response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Approve a campaign')
        def approve(self, request, campaign_id, *args, **kwargs):
                try:
                        # check if campaign exists
                        if not Campaign.objects.filter(id=campaign_id).exists():
                                return Response({"message": "Campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)
                        campaign = Campaign.objects.get(id=campaign_id)
                        campaign.is_active = True
                        campaign.save()
                        return Response({"message": "Campaign approved successfully"}, status=status.HTTP_200_OK)
                except Campaign.DoesNotExist:
                        return Response({"message": "Campaign does not exist"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        
        # View to choose a featured campaign, a random campaign
        @response_schemas(
            response_model=CampaignSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign'], summary='Choose a featured campaign')
        def featured(self, request, *args, **kwargs):
                try:
                        # Get a random campaign
                        now = timezone.now()

                        # Filter campaigns based on your conditions
                        campaigns = Campaign.objects.filter(
                            is_active=True,
                            is_completed=False,
                            is_cancelled=False,
                            is_deleted=False,
                            is_rejected=False,
                            end_date__gte=now,
                        )
                        
                        # Get a list of IDs for campaigns that match the filter
                        campaign_ids = list(campaigns.values_list('id', flat=True))
                        # Randomly choose one ID from the list, if the list is not empty
                        random_id = random.choice(campaign_ids) if campaign_ids else None
                        
                        # Retrieve the campaign corresponding to the randomly chosen ID, if there was one
                        random_campaign = Campaign.objects.get(id=random_id) if random_id else None
                        
                        serializer = CampaignSerializer(random_campaign)
                        response = {
                            "message": "Featured campaign chosen successfully",
                            "data": serializer.data
                        }
                        return Response(response, status=status.HTTP_200_OK)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)