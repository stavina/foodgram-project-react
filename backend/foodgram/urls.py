from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/recipes/', include('api.urls')),
    path('api/', include('rest_framework.urls')),
]
