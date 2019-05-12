from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
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

        onetime_pass = OnetimePass.objects.filter(user_phone=request.POST['phone']).order_by('-id')[0]        
        if request.POST['onetime_pass'] == str(onetime_pass.onetime_pass):
            onetime_pass.confirmed = True
            onetime_pass.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'message':'Неверный пароль, попробуйте запросить новый'},status=status.HTTP_400_BAD_REQUEST)


