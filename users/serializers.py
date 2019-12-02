from rest_framework.serializers import ModelSerializer
from .models import User, Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'photo_url',)


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'profile', 'username', 'last_login',)
