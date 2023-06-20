from django.db import models

from users.models import User

INGREDIENT_NAME_LENGTH = 100
INGREDIENT_MEASUREMENT_LENGTH = 200
TAG_NAME_LENGTH = 200
TAG_COLOR_LENGTH = 7
TAG_SLUG_LENGTH = 200
RECIPE_NAME_LENGTH = 200


class Ingredient(models.Model):
    """Класс ингредиентов."""
    name = models.CharField(
        max_length=INGREDIENT_NAME_LENGTH,
        verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=INGREDIENT_MEASUREMENT_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Класс тегов для рецептов."""
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название'
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        null=True,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        null=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=RECIPE_NAME_LENGTH,
        verbose_name='Название')
    image = models.FileField(
        upload_to='recipe_img/',
        verbose_name='Изображение'
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (минуты)'
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_author_name'
            )
        ]

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Вспомогательная модель ИнгредиентКоличество."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientamount',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientamount',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество в рецепте',
    )

    class Meta:
        verbose_name = 'ИнгредиентКоличество'
        verbose_name_plural = 'ИнгредиентКоличество'
        ordering = ['-recipe']

    def __str__(self):
        return f'Рецепт {self.recipe}, ингредиент {self.ingredient}'


class Favorite(models.Model):
    """Класс добавления рецептов в избранное"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Автор списка избранного'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт из списка избранного'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipes'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe_id} в избранном у {self.user_id}'


class ShoppingCart(models.Model):
    """Класс составления списка покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Автор списка покупок'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Список покупок'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart_user_recipes'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe_id} в списке покупок у {self.user_id}'
