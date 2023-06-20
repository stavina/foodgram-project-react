from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from recipes.models import Ingredient, Recipe, Tag
from .filters import RecipeFilter
from users.models import Subscription

from .serializers import (IngredientsSerializer, RecipesSerializer,
                          TagSerializer, FavoriteSerializer,
                          UserSerializer, UserCreateSerializer,
                          ChangePasswordSerializer, SubscriptionSerializer,
                          SubscriptionSerializer, )

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
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

    """@action(detail=True, methods=['post', 'delete'], url_path='favorite',
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
        return Response(status=status.HTTP_204_NO_CONTENT)"""


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для кастомной модели User."""
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        print(self.action)
        if self.request.method in ('POST', 'PATCH'):
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'],
            permission_classes=[IsAuthenticated])
    def set_password(self, request, *args, **kwargs):
        context = {'request': request}
        user = get_object_or_404(User, pk=request.user.id)
        serializer = ChangePasswordSerializer(
            data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(
                {'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request, context={}, *args, **kwargs):
        context['request'] = self.request
        queryset = User.objects.filter(subscribers__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(page, context=context, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, context={}, *args, **kwargs):
        context['request'] = self.request
        author = get_object_or_404(User, id=kwargs['pk'])
        user = request.user
        if request.method == 'POST':
            Subscription.objects.create(author=author, user=user)
            serializer = UserSerializer(author, context=context)
            return Response(serializer.data, status.HTTP_201_CREATED)

        get_object_or_404(Subscription, author=author, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
