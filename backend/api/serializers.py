from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from recipes.models import (
    Ingredient, IngredientAmount, Recipe, Tag)

User = get_user_model()
MIN_AMOUNT_INGREDIENTS = 1
MIN_COOKING_TIME = 1


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели Юзер."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        role = serializers.CharField(
            read_only=True)

    def validate_role(self, role):
        auth_user = self.context['request'].user
        user = get_object_or_404(
            User,
            username=auth_user)
        if auth_user.is_user:
            role = user.role
        return role


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор авторизации кастомной модели User."""
    password = serializers.CharField(required=True, max_length=128)
    email = serializers.CharField(required=True, max_length=254)


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор смены пароля кастомной модели User."""
    current_password = serializers.CharField(
        error_messages={'required': 'Обязательное поле.'}
    )
    new_password = serializers.CharField(
        error_messages={'required': 'Обязательное поле.'}
    )

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        current_password = validated_data.get('current_password')
        new_password = validated_data.get('new_password')
        if not instance.check_password(current_password):
            raise serializers.ValidationError(
                {
                    'current_password': 'Неверный пароль'
                }
            )
        if current_password == new_password:
            raise serializers.ValidationError(
                {
                    'new_password': 'Новый пароль должен отличаться от '
                                    'текущего пароля'
                }
            )
        instance.set_password(new_password)
        instance.save()
        return validated_data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с кол-вом ингредиентов."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    """Сокращённый сериализатор для рецептов."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    ingredients = IngredientAmountSerializer(many=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField(required=False, allow_null=True)
    cooking_time = serializers.IntegerField(min_value=1)
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'ingredients', 'tags',
                  'cooking_time', 'image')
        read_only_fields = ('id', 'author', 'tags')


class RecipeCreateSerializer(RecipesSerializer):
    """Сериализатор создания рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    cooking_time = serializers.IntegerField(validators=[
        MinValueValidator(MIN_COOKING_TIME,
                          'Минимальное время приготовления - '
                          f'{MIN_COOKING_TIME} минута'),
    ]
    )

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'ingredients', 'tags',
                  'cooking_time', 'image')

    @staticmethod
    def save_ingredients(recipe, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            current_amount = ingredient.get('amount')
            ingredients_list.append(
                IngredientAmount(
                    ingredient=current_ingredient,
                    amount=current_amount
                )
            )
        IngredientAmount.objects.bulk_create(ingredients_list)

    def validate(self, data):
        ingredients_list = []
        ingredients_amount = data.get('ingredients_amount')
        if not ingredients_amount:
            raise serializers.ValidationError(
                'Укажите минимум 1 ингредиент.'
            )
        for ingredient in ingredients_amount:
            ingredients_list.append(ingredient['ingredient']['id'])
        if len(ingredients_list) > len(set(ingredients_list)):
            raise serializers.ValidationError(
                {'error': 'Ингредиенты не должны повторяться.'}
            )
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients_amount')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.set(*tags)
        self.save_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients_amount', None)
        tags = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tags.set(tags)
        if ingredients is not None:
            instance.ingredients.clear()
            self.save_ingredients(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipesSerializer(instance, context=self.context).data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipes.count',
                                             read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'recipes_count', 'recipes')

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user.id
        return obj.subscribers.filter(user=request_user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        limit = request.GET.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSubscriptionSerializer(
            recipes, many=True, context={'request': request})
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FavoriteSerializer(RecipeSubscriptionSerializer):
    """Сериализатор Избранного."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )

    """class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже есть в избранном'
            )
        ]"""


"""class ShoppingCartSerializer(RecipeSubscriptionSerializer):
    (Сериализатор Корзины.)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже есть в корзине'
            )
        ]
"""
