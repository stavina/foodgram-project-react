from django.contrib import admin

from .models import Follow, User

admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
  list_display = ('id', 'username', 'email', 'first_name', 'last_name',)
  search_fields = ('username', 'email',) 
  list_filter = ('email', 'first_name',) 
  empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author', 'user',)
    list_filter = ('author',)
