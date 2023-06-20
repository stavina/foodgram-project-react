from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email',)
    search_fields = ('email', 'username', 'first_name',)
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user',)
