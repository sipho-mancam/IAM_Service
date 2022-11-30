from rest_framework import serializers
from .models import UserProfile



class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=UserProfile
        fields = ['username', 
                'name', 
                'email', 
                'profile_picture', 
                'userId', 
                'friends', 
                'friend_requests',
                'contact_number']
        lookup_field = 'userId'