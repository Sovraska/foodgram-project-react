import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipes.utlis import get_file_path

UserModel = get_user_model()


class TagsModel(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    color = models.CharField(max_length=7, unique=True, verbose_name='Цвет')
    slug = models.SlugField(max_length=100, unique=True)


class IngredientsModel(models.Model):
    title = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=10)
    amount = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)
        ]
    )


class RecipesModel(models.Model):

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор рецепта'
    )
    title = models.CharField(max_length=100, verbose_name='Название')
    image = models.FileField(
        upload_to=get_file_path,
        verbose_name='Изображение'
    )
    description = models.TextField()
    ingredients = models.ManyToManyField(
        IngredientsModel,
        related_name='ingredients',
        verbose_name='Ингредиенты'
    )
    Tag = models.ManyToManyField(
        TagsModel,
        related_name='Tags',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время Готовки',
        validators=[
            MaxValueValidator(500),
            MinValueValidator(1)
        ]
    )


class FavoriteModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    image =
