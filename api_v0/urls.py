from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import *

urlpatterns = [
    url(r'login/$', views.obtain_auth_token),
    url(r'cities/$', CitiesView.as_view()),
    url(r'onetimePass/$', OnetimePassView.as_view()),    
    url(r'confirmOnetimePass/$', ConfirmOnetimePass.as_view()),
    url(r'updateUser/$', UpdateUser.as_view()),
    url(r'categories/$', CategoriesView.as_view()),
    url(r'bids/$', BidsView.as_view()),    
]