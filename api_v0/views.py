from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
#from django.utils.dateparse import parse_date
import datetime
from django.utils.crypto import get_random_string
import random
from rest_framework import status
import re
import requests

from .serializers import *
from main.models import *

# Create your views here.
class CitiesView(APIView):
    def get(self, request):
        cities = Cities.objects.all()
        serializer = CitiesSerializer(cities, many=True)
        return Response(serializer.data)

class OnetimePassView(APIView):
    def get(self, request):            
        onetime_pass = random.randint(1000, 9999)
        phone_tpl = '\d{11}$'
        if 'phone' not in request.GET:
            return Response({'message': 'Введите номер телефона'}, status=status.HTTP_400_BAD_REQUEST)
        if re.match(phone_tpl, request.GET['phone']) is None:
            return Response({'message': 'Неверный формат номера телефона'}, status=status.HTTP_400_BAD_REQUEST)
        
        new_onetime_pass = OnetimePass(
            user_phone = request.GET['phone'],
            onetime_pass = onetime_pass
        )
        new_onetime_pass.save()
        
        requests.post("https://gate.smsaero.ru/send/?user=zuev-egor@inbox.ru&password=9iH9TOaRx2zJGPTC3yjogBArodc&type=3&to=" +
                        request.GET['phone'] + "&text=Код активации: " + str(onetime_pass) + "&from=Moika+SAM")
        return Response(status=status.HTTP_200_OK)

class ConfirmOnetimePass(APIView):
    def post(self, request):
        phone_tpl = '\d{11}$'
        if 'phone' not in request.POST:
            return Response({'message': 'Не указан номер телефона'}, status=status.HTTP_400_BAD_REQUEST)
        if re.match(phone_tpl, request.POST['phone']) is None:
            return Response({'message': 'Неверный формат номера телефона'}, status=status.HTTP_400_BAD_REQUEST)

        ##СДЕЛАТЬ TRY CATCH на запись в бд
        onetime_pass = OnetimePass.objects.filter(user_phone=request.POST['phone']).order_by('-id')[0]        
        if request.POST['onetime_pass'] == str(onetime_pass.onetime_pass) and not onetime_pass.confirmed:
            onetime_pass.confirmed = True
            onetime_pass.save()
            existing_user = 'Y'
            user_info = []
            try:
                user = get_user_model().objects.get(phone=request.POST['phone'])
                user_info.append({
                    'city':user.city.name,
                    'date_of_birth':user.date_of_birth.strftime('%d.%m.%y'),
                    'sex':user.sex,
                    'name':user.name,
                })                                
            except get_user_model().DoesNotExist:
                new_pass = get_random_string(length=9)
                user = get_user_model().objects.create(
                    phone = request.POST['phone'],
                    password = new_pass,
                    is_system_user=False,
                )
                existing_user = 'N'                    
            token = Token.objects.get_or_create(user=user)
            return Response({'token':str(token[0]), 'existing_user':existing_user, 'user_info':user_info}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Неверный пароль, попробуйте запросить новый'},status=status.HTTP_400_BAD_REQUEST)

class UpdateUser(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request):        
        
        if 'birth_date' not in request.POST or request.POST['birth_date']=="":
            return Response ({'message':'Не указана дата рождения'},status=status.HTTP_400_BAD_REQUEST)

        if 'name' not in request.POST or request.POST['name']=="":
            return Response ({'message':'Не указано имя'},status=status.HTTP_400_BAD_REQUEST)
        
        if 'city_id' not in request.POST or request.POST['city_id']=="":
            return Response ({'message':'Не выбран город'},status=status.HTTP_400_BAD_REQUEST)
        
        if 'sex' not in request.POST or request.POST['sex']=="":
            return Response ({'message':'Не указан пол'},status=status.HTTP_400_BAD_REQUEST)

        user = request.user        
        
        str_birth_date = request.POST['birth_date']        
        datetime_obj = datetime.datetime.strptime(str_birth_date, '%d.%m.%Y')

        user.date_of_birth = datetime_obj
        user.city = Cities.objects.get(pk=int(request.POST['city_id']))
        user.sex = request.POST['sex']
        user.name = request.POST['name']
        
        user.save()        
        return Response(status=status.HTTP_200_OK)

class CategoriesView(APIView):
    def get(self, request):        
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

class BidsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user

        if 'accept_bid' in request.POST and int(request.POST['accept_bid']) == 1:            
            if 'id' not in request.POST or request.POST['id']=="":
                return Response ({'message':'Что-то пошло не так, скорее всего нет ID заявки'},status=status.HTTP_400_BAD_REQUEST)
            try:
                bid = Bids.objects.get(pk=int(request.POST['id']))
                if bid.user == user and not bid.offer_accept:                    
                    bid.offer_accept = True
                    bid.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({'message':'Что-то пошло не так'}, status=status.HTTP_400_BAD_REQUEST)

            except Bids.DoesNotExist:
                return Response({'message':'Что то пошло не так, такой заявки нет'}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'cancel_bid' in request.POST and int(request.POST['cancel_bid']) == 1:
            if 'id' not in request.POST or request.POST['id']=="":
                return Response ({'message':'Что-то пошло не так, скорее всего нет ID заявки'},status=status.HTTP_400_BAD_REQUEST)
            try:
                bid = Bids.objects.get(pk=int(request.POST['id']))
                if bid.user == user and not bid.offer_accept:                    
                    bid.offer_canceled = True
                    bid.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({'message':'Отмена заявки. Что-то пошло не так'}, status=status.HTTP_400_BAD_REQUEST)
            except Bids.DoesNotExist:
                return Response({'message':'Что то пошло не так, такой заявки нет'}, status=status.HTTP_400_BAD_REQUEST)

        if 'wish' not in request.POST or request.POST['wish']=="":
            return Response ({'message':'Сообщите нам свои пожелания :)'},status=status.HTTP_400_BAD_REQUEST)
        
        if 'wish_date' not in request.POST or request.POST['wish_date']=="":
            return Response ({'message':'Укажите дату'},status=status.HTTP_400_BAD_REQUEST)        
        
        datetime_obj = datetime.datetime.strptime(request.POST['wish_date'], '%d.%m.%Y')
        new_bid = Bids (
            user = user,
            category = Categories.objects.get(pk=int(request.POST['category'])),
            wish = request.POST['wish'],
            wish_date = datetime_obj,
        )
        new_bid.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        if 'id' in request.GET and request.GET['id'] != "":            
            try:
                bid = Bids.objects.get(pk=int(request.GET['id']))
                if bid.user == user:
                    serializer = DetailBidSerializer(bid)
                    return Response(serializer.data)
                else:
                    return Response({'message':'Что-то пошло не так'}, status=status.HTTP_400_BAD_REQUEST)
            except Bids.DoesNotExist:
                return Response({'message':'Что то пошло не так, Олежик. Это бэд реквест, выпей таблеточку.'}, status=status.HTTP_400_BAD_REQUEST)            
        else:
            bids = Bids.objects.filter(user=user, offer_sent=True, offer_accept=False, offer_canceled=False)
            serializer = BidsSerializer(bids, many=True)
            return Response(serializer.data)

class OfferView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = request.user
        if 'id' in request.GET and request.GET['id'] != "":            
            try:
                offer = Offer.objects.get(pk=int(request.GET['id']))
                if offer.bid.user == user:
                    serializer = DetailOfferSerializer(offer)
                    return Response(serializer.data)
                else:
                    return Response({'message':'Что-то пошло не так'}, status=status.HTTP_400_BAD_REQUEST)
            except Bids.DoesNotExist:
                return Response({'message':'Что то пошло не так, Олежик. Это бэд реквест, выпей таблеточку.'}, status=status.HTTP_400_BAD_REQUEST)            
        else:
            offers = Offer.objects.filter(user=user, accept=False, canceled=False)
            serializer = OfferListSerializer(offers, many=True)
            return Response(serializer.data)
