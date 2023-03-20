from django.contrib import admin

from .models import IngredientsModel, TagsModel, RecipesModel


@admin.register(IngredientsModel)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'measurement_unit',
    )
    search_fields = (
        'title',
    )


@admin.register(TagsModel)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'color',
        'slug'
    )
    search_fields = (
        'title',
    )


@admin.register(RecipesModel)
class RecipesAdmin(admin.ModelAdmin):
    readonly_fields = ('chosen_count',)
    list_display = (
        'title',
        'author',
        'chosen_count',
    )
    search_fields = (
        'title',
        'author',
        'tags'
    )

    def chosen_count(self, obj):
        if obj:
            return 1
        return '--Избранных нет--'

    chosen_count.short_description = 'аватар'




