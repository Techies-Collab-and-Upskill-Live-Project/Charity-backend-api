from rest_framework.viewsets import GenericViewSet
from core.exception_handlers import response_schemas
from .serializers import CampaignCategorySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import CampaignCategory
from drf_spectacular.utils import extend_schema
import uuid


class CampaignCategoryView(GenericViewSet):
        serializer_class = CampaignCategorySerializer

        @response_schemas(
            response_model=CampaignCategorySerializer, code=201, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign Category'], summary='Create a new campaign category')
        def create(self, request, *args, **kwargs):
                serializer = CampaignCategorySerializer(data=request.data)

                serializer.is_valid(raise_exception=True)

                # Retrieve the validated data
                validated_data = serializer.validated_data

                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        # View to get all campaign categories
        @response_schemas(
            response_model=CampaignCategorySerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign Category'], summary='Get all campaign categories')
        def list(self, request, *args, **kwargs):
                campaign_categories = CampaignCategory.objects.all()
                serializer = CampaignCategorySerializer(campaign_categories, many=True)
                # Calculate the count of campaign categories
                count = len(campaign_categories)

                # Create a dictionary including both the serialized data and the count
                response_data = {
                    "campaign_categories": serializer.data,
                    "count": count,
                    "message": "All campaign categories retrieved successfully"
                }

                return Response(response_data, status=status.HTTP_200_OK)

        # View to get a single campaign category
        @response_schemas(
            response_model=CampaignCategorySerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign Category'], summary='Get a single campaign category')
        def retrieve(self, request, pk, *args, **kwargs):
                try:
                        # # check if the uuid is valid
                        # uuid_obj = uuid.UUID(pk)
                        # print(uuid_obj)
                        campaign_category = CampaignCategory.objects.get(id=pk)
                        if not campaign_category:
                                return Response({"message": "Campaign category not found"}, status=status.HTTP_404_NOT_FOUND)
                        serializer = CampaignCategorySerializer(campaign_category)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except (ValueError, CampaignCategory.DoesNotExist):
                        return Response({"message": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # View to update a campaign category
        @response_schemas(
            response_model=CampaignCategorySerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign Category'], summary='Update a campaign category')
        def update(self, request, pk, *args, **kwargs):
                try:
                        campaign_category = CampaignCategory.objects.get(id=pk)
                        if not campaign_category:
                                return Response({"message": "Campaign category not found"}, status=status.HTTP_404_NOT_FOUND)
                        serializer = CampaignCategorySerializer(campaign_category, data=request.data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # View to delete a campaign category
        @response_schemas(
            response_model=CampaignCategorySerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Campaign Category'], summary='Delete a campaign category')
        def destroy(self, request, pk, *args, **kwargs):
                try:
                        campaign_category = CampaignCategory.objects.get(id=pk)
                        if not campaign_category:
                                return Response({"message": "Campaign category not found"}, status=status.HTTP_404_NOT_FOUND)
                        campaign_category.delete()
                        return Response({"message": "Campaign category deleted successfully"}, status=status.HTTP_200_OK)
                except Exception as e:
                        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

