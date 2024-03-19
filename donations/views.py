from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from core.exception_handlers import response_schemas
from .serializers import DonationsSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Donation

# Create your views here.


class DonationsView(GenericViewSet):
        serializer_class = DonationsSerializer

        permission_classes = [IsAuthenticated]
        
        # View to create a new doantion using the campaign ID

        @response_schemas(
            response_model=DonationsSerializer, code=201, schema_response_codes=[400]
        )
        @extend_schema(tags=['Donations'], summary='Create a new donation')
        def create(self, request, *args, **kwargs):
            data = request.data.copy()
            data['donor_id'] = request.user.id
            print("data: ", data)
            serializer = DonationsSerializer(data=data, context={'request': request})

            serializer.is_valid(raise_exception=True)

            # Retrieve the validated data
            validated_data = serializer.validated_data

            serializer.save()

            response = {
                "donation": serializer.data,
                "message": "Donation created successfully"
            }

            return Response(response, status=status.HTTP_201_CREATED)

        # View to list all donations made by the authenticated user

        @response_schemas(
            response_model=DonationsSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Donations'], summary='Get all donations')
        def list(self, request, *args, **kwargs):
            try:
                donations = Donation.objects.all()
                serializer = DonationsSerializer(donations, many=True)
                # Calculate the count of donations
                count = len(donations)

                # Create a dictionary including both the serialized data and the count
                response_data = {
                    "donations": serializer.data,
                    "count": count,
                    "message": "All donations retrieved successfully"
                }

                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        
        # View to retrieve a single donation using the donation ID

        @response_schemas(
            response_model=DonationsSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Donations'], summary='Get a single donation')
        def retrieve(self, request, donation_id, *args, **kwargs):
            try:

                donation = Donation.objects.get(id=donation_id)
                serializer = DonationsSerializer(donation)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Donation.DoesNotExist:
                return Response({"message": "Donation does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        
        # View to delete a single donation using the donation ID

        @response_schemas(
            response_model=DonationsSerializer, code=200, schema_response_codes=[400]
        )
        @extend_schema(tags=['Donations'], summary='Delete a single donation')
        def destroy(self, request, donation_id, *args, **kwargs):
            try:
                donation = Donation.objects.get(id=donation_id)
                donation.delete()
                return Response({"message": "Donation deleted successfully"}, status=status.HTTP_200_OK)
            except Donation.DoesNotExist:
                return Response({"message": "Donation does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(
                    {
                        "message": str(e)
                    },
                    status=status.HTTP_400_BAD_REQUEST)