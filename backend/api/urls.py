from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (DownloadShoppingCartViewSet, FavoriteRecipeViewSet,
                    IngredientsViewSet, RecipeViewSet, ShoppingCartViewSet,
                    TagsViewSet, UsersViewSet)

router_v1 = DefaultRouter()

router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('recipes', DownloadShoppingCartViewSet,
                   basename='download_shopping_cart')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('recipes', FavoriteRecipeViewSet,
                   basename='favorite_recipes')
router_v1.register('recipes', ShoppingCartViewSet, basename='shopping_cart')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
