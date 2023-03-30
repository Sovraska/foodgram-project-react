from django.contrib import admin
from .models import (Favorite, IngredientsModel, RecipeIngredient,
                     RecipesModel, Shopping, TagsModel)


@admin.register(IngredientsModel)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )


@admin.register(TagsModel)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )
    search_fields = (
        'name',
    )


@admin.register(RecipesModel)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'image',
        'view_text',
        'cooking_time'
    )
    search_fields = (
        'name',
        'author',
        'tags'
    )

    def view_text(self, obj):
        return obj.text[:100]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = (
        'ingredient',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
    )


@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
    )
