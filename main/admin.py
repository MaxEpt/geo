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
        'create_date',
        'wish',
        'wish_date',
        'finished',        
    ]

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = [        
        'bid',
        'short_desc',
        'otype',
        'place',
        'accept',
        'canceled',
        'sent_date'
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