from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from main.models import *

class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ("id", "name","latitude", "longitude")

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("id", "cat_name","image")

class PlaceSerializer(serializers.ModelSerializer):    
     class Meta:
        model = Place
        fields = ("id", "name")

class DetailPlaceSerializer(serializers.ModelSerializer):    
     category = CategoriesSerializer()
     class Meta:
        model = Place
        fields = ("id", "name", "description", "address", "image", "category")   

class BidsSerializer(serializers.ModelSerializer):
    offer_place = PlaceSerializer()
    class Meta:
        model = Bids
        fields = ("id", "short_desc","offer_place","offer_type")

class DetailBidSerializer(serializers.ModelSerializer):
    offer_place = DetailPlaceSerializer()
    class Meta:
        model = Bids
        fields = ("offer_place", "offer_text")
