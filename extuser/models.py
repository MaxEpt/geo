from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError('Номер телефона обязателен')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(phone, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class ExtUser(AbstractBaseUser, PermissionsMixin):

    phone = models.CharField(
        'Номер телефона',
        max_length=11,
        unique=True,
        db_index=True
    )

    register_date = models.DateField(
        'Дата регистрации',
        auto_now_add=True
    )
    is_active = models.BooleanField(
        'Активен',
        default=True
    )
    is_admin = models.BooleanField(
        'Суперпользователь',
        default=False
    )
    is_system_user = models.BooleanField('Системный пользователь', default=False)


    # Этот метод обязательно должен быть определён
    def get_full_name(self):
        return self.phone

    # Требуется для админки
    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.phone

    def __str__(self):
        return self.phone
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
