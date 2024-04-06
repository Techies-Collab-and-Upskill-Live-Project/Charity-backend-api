from rest_framework import serializers
from customauth.models import CustomUser as User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
