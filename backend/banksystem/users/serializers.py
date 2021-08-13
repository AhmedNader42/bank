from rest_framework import serializers
from .models import User
from dj_rest_auth.serializers import UserDetailsSerializer
from django.conf import settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer

"""
    Add a a user_type to the default user 
"""
class CustomRegisterSerializer(RegisterSerializer):
    user_type = serializers.IntegerField()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['user_type'] = self.validated_data.get('user_type', '')
        return data_dict


class CustomUserDetailsSerializer(UserDetailsSerializer):

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('user_type',)
