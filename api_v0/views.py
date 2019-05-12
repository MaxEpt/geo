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
        requests.post("https://gate.smsaero.ru/send/?user=zuev-egor@inbox.ru&password=9iH9TOaRx2zJGPTC3yjogBArodc&type=3&to=" +
                        request.GET['phone'] + "&text=Код активации: " + str(onetime_pass) + "&from=Moika+SAM")
        return Response(status=status.HTTP_200_OK)