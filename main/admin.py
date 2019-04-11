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
        'offer_text',
        'offer_sent',
        'offer_accept',
    ]
