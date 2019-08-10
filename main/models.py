from django.db import models
from django.conf import settings
from unixtimestampfield.fields import UnixTimeStampField
# Create your models here.
class Categories(models.Model):
    cat_name = models.CharField('Название категории', max_length=150)
    image = models.FileField(blank=True)
    def __str__(self):
        return self.cat_name
    class Meta:        
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Cities(models.Model):
    name = models.CharField('Название', max_length=50)
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    def __str__(self):
        return self.name
    class Meta:        
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Place(models.Model):
    name = models.CharField("Название", max_length = 100)
    address = models.CharField("Адрес", max_length = 100)
    image = models.FileField("Изображение")
    city = models.ForeignKey(Cities, on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    description = models.TextField("Описание")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Менеджер", on_delete=models.PROTECT, blank=True, default=None)
    def __str__(self):
        return self.name
    class Meta:        
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'
        
class Bids(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    wish = models.TextField('Пожелание')
    wish_date = models.DateField('Желаемая дата', default=None)   
    create_date = models.DateTimeField('Время создания заявки', auto_now_add=True)
    finished = models.BooleanField('Заявка закрыта', default=False)
    class Meta:        
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-create_date']

class Offer(models.Model):    
    bid = models.ForeignKey(Bids, on_delete=models.PROTECT)
    short_desc = models.CharField('Краткое описание', max_length=100, default="")
    text = models.TextField('Предложение')
    offer_CHOICES = ((0, 'Подарок'), (1, 'Скидка'))
    otype = models.IntegerField('Тип предложения', choices=offer_CHOICES, default=0)
    place = models.ForeignKey(Place, on_delete=models.PROTECT, null=True)
    accept = models.BooleanField('Предложение принятно', default=False)
    canceled = models.BooleanField('Предложение отклонено', default=False)
    sent_date = models.DateTimeField('Время отправки предложения', blank=True, null=True, auto_now_add=True)
    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
        ordering = ['-sent_date','-accept']

class OnetimePass(models.Model):
    user_phone = models.CharField("Номер телефона", max_length=11, default="")
    onetime_pass = models.IntegerField("Одноразовый пароль")
    confirmed = models.BooleanField("Подтвержден", default=False)
    created_at = UnixTimeStampField("timestamp", auto_now_add=True)
    class Meta:        
        verbose_name = 'Одноразовый пароль'
        verbose_name_plural = 'Одноразовые пароли'

class NotificationSetting(models.Model):
    admin_email = models.CharField("E-Mail администратора", max_length=100, default="")
    class Meta:
        verbose_name = 'Настройка уведомлений'
        verbose_name_plural = 'Настройки уведомлений' 



        