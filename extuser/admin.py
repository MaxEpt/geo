from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import UserChangeForm
from .forms import UserCreationForm
from .models import ExtUser


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        'phone',
        'register_date',
        'is_admin',
        'is_active',
        'is_system_user',
        'date_of_birth',
        'city',
    ]

    list_filter = ('is_admin', 'register_date', 'is_active')

    fieldsets = (
                (None, {'fields': ('phone', 'password', 'is_system_user', 'city')}),
                ('Permissions', {'fields': ('is_admin',)}),
                ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone',
                'password1',
                'password2'
            )}
         ),
    )

    search_fields = ('phone',)
    ordering = ('register_date',)
    filter_horizontal = ()

# Регистрация нашей модели
admin.site.register(ExtUser, UserAdmin)
admin.site.unregister(Group)