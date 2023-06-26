from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models.functions import Length

from api.constants import (MIN_AMOUNT_INGREDIENTS, MIN_COOKING_TIME,
                           RECIPE_NAME_LENGTH, TAG_COLOR_LENGTH,
                           TAG_NAME_LENGTH, TAG_SLUG_LENGTH)
from users.models import User

models.CharField.register_lookup(Length)


class Ingredient(models.Model):
    """Класс игредиентов."""
    name = models.CharField(
        blank=False,
        max_length=150,
        db_index=True,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=150,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name - пустое значение\n',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__length__gt=0),
                name='\n%(app_label)s_%(class)s_measurement_unit - пустое'
                     'значение\n',
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Класс тегов для рецептов."""
    name = models.CharField(
        unique=True,
        max_length=TAG_NAME_LENGTH,
    )
    color = models.CharField(
        unique=True,
        max_length=TAG_COLOR_LENGTH,
        verbose_name='Цвет в HEX-формате',
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Поле должно содержать цвет в HEX-формате.'
            )
        ]

    )
    slug = models.SlugField(
        unique=True,
        max_length=TAG_SLUG_LENGTH,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class QuerySet(models.QuerySet):
    """Класс для добавления избранного и списка корзины."""

    def add_annotations(self, user_id):
        return self.annotate(
            is_favorited=models.Exists(
                Favorite.objects.filter(
                    recipe__pk=models.OuterRef('pk'),
                    user_id=user_id,
                )
            ),
            is_in_shopping_cart=models.Exists(
                ShoppingCart.objects.filter(
                    recipe__pk=models.OuterRef('pk'),
                    user_id=user_id,
                )
            ),
        )


class Recipe(models.Model):
    """Класс рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=RECIPE_NAME_LENGTH,
        db_index=True,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        blank=True,
        upload_to='recipes/images/',
        verbose_name='Фото'
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Список ингредиентов',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                'Минимальное время приготовления - '
                f'{MIN_COOKING_TIME} минута'),
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    objects = QuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_for_author',
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name - пустое значение\n',
            ),
        )

    def __str__(self):
        return f'{self.name} от {self.author.username}'


class IngredientAmount(models.Model):
    """Модель показывает кол-во ингредиентов."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=MIN_AMOUNT_INGREDIENTS,
        validators=[
            MinValueValidator(
                MIN_AMOUNT_INGREDIENTS,
                'Минимальное количество ингредиентов - '
                f'{MIN_AMOUNT_INGREDIENTS} ед.'),
        ],
    )


class Favorite(models.Model):
    """Класс добавления рецептов в избранное."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Автор списка избранного',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт из списка избранного',
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления в избранное',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_for_favorite'
            ),
        )


class ShoppingCart(models.Model):
    """Класс составления списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Автор списка покупок',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления в список покупок',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'В корзине'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )
