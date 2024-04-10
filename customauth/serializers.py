from django.contrib.auth import password_validation
from .models import UserProfile
from django.db.models import Sum

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from donations.models import Donation
from donations.serializers import DonationsSerializer
from campaign.models import Campaign
from campaign.serializers import CampaignSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password')

    def validate(self, data):
        password = data.get('password')
        validate_password(password)
        return data

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        # Check if a user with the same email already exists
        existing_user = get_user_model().objects.filter(email=email).first()
        if existing_user:
            raise serializers.ValidationError({"email": ["User with this email already exists."]})

        # If no existing user, proceed with creating the new user
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        refresh = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    donations = serializers.SerializerMethodField()
    total_donations = serializers.SerializerMethodField(read_only=True)
    campaigns = serializers.SerializerMethodField()
    total_campaigns = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'name', 'about', 'profile_photo', 'short_description', 'instagram_link', 'facebook_link', 'twitter_link', 'donations', 'total_donations', 'campaigns', 'total_campaigns')
    
     # Get all donations by id
    def get_donations(self, obj):
        # Fetch donations by the user profile, assuming a ForeignKey from Donation to UserProfile
        donations = Donation.objects.filter(donor_id=obj)
        return DonationsSerializer(donations, many=True).data
    
    def get_total_donations(self, obj):
        total = Donation.objects.filter(donor_id=obj.id).aggregate(total=Sum('amount'))['total']
        return total if total is not None else 0
    
    def get_campaigns(self, obj):
        campaigns = Campaign.objects.filter(user_profile=obj)
        return CampaignSerializer(campaigns, many=True).data
    
    def get_total_campaigns(self, obj):
        total = Campaign.objects.filter(user_profile=obj.id).count()
        return total if total is not None else 0

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    new_password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'about', 'short_description', 'instagram_link', 'facebook_link', 'twitter_link', 'profile_photo', 'current_password', 'new_password', 'new_password2', 'name')

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        new_password2 = data.get('new_password2')


        if (new_password or new_password2) and not current_password:
            raise serializers.ValidationError("Current password is required to change the password.")

        if current_password and not self.instance.user.check_password(current_password):
            raise serializers.ValidationError("Incorrect current password.")

        if new_password and new_password2 and new_password != new_password2:
            raise serializers.ValidationError("New passwords do not match.")

        if new_password:
            password_validation.validate_password(new_password, self.instance.user)

        return data

    def update(self, instance, validated_data):
        # valid_attributes = [
        #     'first_name', 'last_name', 'about', 'short_description',
        #     'instagram_link', 'facebook_link', 'twitter_link', 'profile_photo', 'new_password'
        # ]

        # for key in validated_data.keys():
        #     if key not in valid_attributes:
        #         raise ValidationError(f"Invalid attribute '{key}'")
            
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.about = validated_data.get('about', instance.about)
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.instagram_link = validated_data.get('instagram_link', instance.instagram_link)
        instance.facebook_link = validated_data.get('facebook_link', instance.facebook_link)
        instance.twitter_link = validated_data.get('twitter_link', instance.twitter_link)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)

        new_password = validated_data.get('new_password')
        if new_password:
            instance.user.set_password(new_password)
            instance.user.save()

        # # Combine first and last names or set to an empty string if both are None
        # instance.name = f"{instance.first_name} {instance.last_name}".strip() or ''

        instance.save()
        return instance