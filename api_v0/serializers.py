from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from main.models import *

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ("id", "namelatitude", "longitude")