from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet,
                    TagViewSet, CustomUserViewSet)

app_name = 'api'

router_v1_auth = routers.DefaultRouter()
router_v1 = routers.DefaultRouter()

router_v1_auth.register('token/login', CustomUserViewSet, basename='login')
router_v1_auth.register('token/logout', CustomUserViewSet, basename='logout')

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register(
    'users/subscriptions',
    CustomUserViewSet,
    basename='subscriptions_list'
)
router_v1.register(
    r'users/(?P<id>\d+)/subscribe',
    CustomUserViewSet,
    basename='subscribe'
)
router_v1.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('auth/', include(router_v1_auth.urls)),
    path('', include(router_v1.urls)),
]
