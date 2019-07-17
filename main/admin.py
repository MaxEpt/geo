from django.contrib import admin
from main.models import *
# Register your models here.

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['cat_name']

@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'category',
        'bid_create_date',
        'wish',
        'wish_date',
        'offer_text',
        'offer_sent',
        'offer_accept',
        'offer_canceled',
        'offer_type',        
    ]

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'longitude',
        'latitude',
    ]

@admin.register(OnetimePass)
class OnetimePassAdmin(admin.ModelAdmin):
    list_display = [
        'user_phone',
        'onetime_pass',
        'created_at',
        'confirmed',
    ]


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'city',
        'category',        
    ]
@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = [
        'admin_email'
    ]