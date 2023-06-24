import os

from django.contrib import admin
from dotenv import load_dotenv


from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)

load_dotenv()

MIN_AMOUNT_INGREDIENTS = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Отображение тэгов."""
    list_display = ('name', 'slug', 'color')
    search_fields = ('name',)
    empty_value_display = os.getenv('VALUE_DISPLAY', '---')


class IngredientInline(admin.TabularInline):
    model = IngredientAmount
    extra = 0
    min_num = MIN_AMOUNT_INGREDIENTS


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Отображение ингридиентов."""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name',)
    save_on_top = True
    empty_value_display = os.getenv('VALUE_DISPLAY', '---')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Отображение рецептов."""
    list_display = ('author', 'name', 'cooking_time', 'count_favorites')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientInline,)
    empty_value_display = os.getenv('VALUE_DISPLAY', '---')

    def count_favorites(self, obj):
        return obj.favorite.count()

    count_favorites.short_description = "Добавлено в избранное"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Отображение подписок на авторов."""
    list_display = ('user', 'recipe')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = os.getenv('VALUE_DISPLAY', '---')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Отображение списка покупок."""
    list_display = ('id', 'recipe', 'user')
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = os.getenv('VALUE_DISPLAY', '---')


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    """Отображение кол-ва ингредиентов в рецептах."""
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    search_fields = ('recipe',)
