from django.db import models
from django.conf import settings
from unixtimestampfield.fields import UnixTimeStampField
# Create your models here.
class Categories(models.Model):
    cat_name = models.CharField('Название категории', max_length=150)
    def __str__(self):
        return self.cat_name
    class Meta:        
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Bids(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    wish = models.TextField('Пожелание')    
    offer_text = models.CharField('Предложение', max_length=200)
    offer_sent = models.BooleanField('Предложение отправлено',default=False)
    offer_accept = models.BooleanField('Предложение принятно', default=False)
    bid_create_date = models.DateTimeField('Время создания заявки', auto_now_add=True)
    offer_sent_date = models.DateTimeField('Время отправки предложения', auto_now_add=True)
    class Meta:        
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-bid_create_date']


class Cities(models.Model):
    name = models.CharField('Название', max_length=50)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    class Meta:        
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class OnetimePass(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    onetime_pass = models.IntegerField("Одноразовый пароль")
    confirmed = models.BooleanField('Подтвержден', default=False)
    created_at = UnixTimeStampField("timestamp", auto_now_add=True)
    class Meta:        
        verbose_name = 'Одноразовый пароль'
        verbose_name_plural = 'Одноразовые пароли'
        