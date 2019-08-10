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
        
        bids_id = []#for exclude from bids
        offers = Offer.objects.filter(place=place)
        
        resp = {'offers':[],'bids':[]}
        for offer in offers:
            bids_id.append(offer.bid.id)
            phone = "-"
            if offer.accept:
                phone = offer.bid.user.phone
            resp['offers'].append({
                'user_phone':phone,
                'user_sex':offer.bid.user.sex,
                'user_date_of_birth':offer.bid.user.date_of_birth,
                'user_name':offer.bid.user.name,
                'wish_date':offer.bid.wish_date,
                'wish':offer.bid.wish,
                'accept':offer.accept,
                'canceled':offer.canceled,
                'type':offer.otype,
                'short_desc':offer.short_desc,
                'sent_date':offer.sent_date,
            })
                        
        
        bids = Bids.objects.filter(user__city=place.city, category=place.category, finished=False).exclude(id__in=bids_id)
        
        
        for bid in bids:  
            resp['bids'].append({
                'bid_id':bid.id,                
                'user_sex':bid.user.sex,
                'user_date_of_birth':bid.user.date_of_birth,
                'user_name':bid.user.name,
                'wish_date':bid.wish_date,
                'create_date':bid.create_date,                          
                'wish':bid.wish,             
                
            })        
        return Response(resp)

    def post(self, request):
        place = Place.objects.get( manager=request.user ) 
        if 'id' in request.POST and request.POST['id'] != "":
            bid  = Bids.objects.get(id=request.POST['id'])
            if bid.user.city==place.city and bid.category==place.category and not bid.finished:
                if 'short_desc' not in request.POST or request.POST['short_desc']=="":
                    return Response({'message':'Не заполнено краткое описание'}, status=status.HTTP_400_BAD_REQUEST) 
                if 'text' not in request.POST or request.POST['text']=="":
                    return Response({'message':'Не заполнен текст предложения'}, status=status.HTTP_400_BAD_REQUEST) 
                if 'offer_type' not in request.POST or request.POST['offer_type']=="":
                    return Response({'message':'Не выбран тип предложения'}, status=status.HTTP_400_BAD_REQUEST) 

                new_offer = Offer(
                    bid=bid,
                    short_desc=request.POST['short_desc'],
                    text=request.POST['text'],
                    otype=int(request.POST['offer_type']),
                    place=place,
                )
                new_offer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'message':'Что то пошло не так'}, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({'message':'Не передан ID заявки'}, status=status.HTTP_400_BAD_REQUEST) 