from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import datetime
from rest_framework import status
from .serializers import *
from main.models import *

class ManagerBidsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        place = Place.objects.get(id=1)        
        bids = Bids.objects.filter(user__city=place.city, category=place.category)
        #serializer = ManagerBidsSerializer(bids, many=True)
        for bid in bids:
            print('123')
            print(str(bid.user.date_of_birth))
        return Response({"status:ok"})