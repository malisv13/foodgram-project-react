from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'pk',
        'email',
        'password',
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'email')
    search_fields = ('username',)
    empty_value_display = '-пусто-'


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', )
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'
