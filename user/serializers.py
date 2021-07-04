"""
    User Application Serializers
    user/serializers.py
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ User serializer """
    class Meta:
        """ Meta """
        model = get_user_model()
        fields = ('id', 'username', 'name', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
