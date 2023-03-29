from django.contrib import admin

from .models import IngredientsModel, TagsModel, RecipesModel


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
    readonly_fields = ('chosen_count',)
    list_display = (
        'name',
        'author',
        'chosen_count',
    )
    search_fields = (
        'name',
        'author',
        'tags'
    )

    def chosen_count(self, obj):
        if obj:
            return 1
        return '--Избранных нет--'

    chosen_count.short_description = 'аватар'




