from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from recipes.models import ShoppingCart, Ingredient, Recipe, Tag
from .filters import RecipeFilter

from .serializers import (ShoppingCartSerializer,
                          IngredientsSerializer, RecipesSerializer,
                          TagSerializer, FavoriteSerializer)

User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели тегов."""
    permission_classes = (AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели ингредиентов."""
    permission_classes = (AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            return self.queryset.filter(
                name__icontains=name)
        return super().queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели рецептов."""
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = FavoriteSerializer(data={'user': request.user.id,
                                                  'recipe': recipe.id})
            return Response(serializer.data, status.HTTP_201_CREATED)

    @action(detail=True, methods=['post', 'delete'], url_path='favorite',
            url_name='favorite',
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(data={'user': request.user.id,
                                                      'recipe': recipe.id})
            return Response(serializer.data, status.HTTP_201_CREATED)

        get_object_or_404(ShoppingCart, recipe=recipe, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
