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
        place = Place.objects.get( manager=request.user ) 
        
        bids = Bids.objects.filter(user__city=place.city, category=place.category)
        resp = []
        for bid in bids:            
            user_phone = "-"
            if bid.offer_accept:
                user_phone = bid.user.phone 
                
            if bid.offer_accept and not bid.offer_place==place:
                continue
            
            resp.append({
                'bid_id':bid.id,
                'user_phone':user_phone,
                'user_sex':bid.user.sex,
                'user_date_of_birth':bid.user.date_of_birth,
                'user_name':bid.user.name,
                'wish_date':bid.wish_date,
                'bid_create_date':bid.bid_create_date,
                'offer_sent_date':bid.offer_sent_date,
                'offer_accept':bid.offer_accept,
                'wish':bid.wish,
                'offer_canceled':bid.offer_canceled,
                'offer_sent':bid.offer_sent,                                
            })
        
        return Response(resp)