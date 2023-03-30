import json
from contextlib import closing

import psycopg2
from django.shortcuts import get_object_or_404
from psycopg2 import Error
from rest_framework import status
from rest_framework.response import Response

from recipes.models import RecipesModel


def insert_into_base_ingredients():
    try:
        with closing(psycopg2.connect(
                dbname='postgres',
                user="postgres",
                password='postgres',
                host='db',
                port=5432
        )) as conn:
            with conn.cursor() as cursor:
                with open(
                        './data/ingredients.json',
                        'r',
                        encoding='utf8'
                ) as json_file:
                    data = json.load(json_file)
                    for line in data:
                        title = line.get('name')
                        measurement_unit = line.get('measurement_unit')
                        cursor.execute(
                            f"INSERT INTO recipes_ingredientsmodel("
                            f"name, measurement_unit"
                            f") VALUES ('{title}', '{measurement_unit}');")
                        conn.commit()
                    for i in cursor:
                        print(i)
        print("Соединение с PostgreSQL закрыто")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def post(request, pk, model, serializer):
    recipe = get_object_or_404(RecipesModel, pk=pk)
    if model.objects.filter(user=request.user, recipe=recipe).exists():
        return Response(
            {'errors': 'Рецепт уже есть в избранном/списке покупок'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    model.objects.get_or_create(user=request.user, recipe=recipe)
    data = serializer(recipe).data
    return Response(data, status=status.HTTP_201_CREATED)


def delete(request, pk, model):
    recipe = get_object_or_404(RecipesModel, pk=pk)
    if model.objects.filter(user=request.user, recipe=recipe).exists():
        follow = get_object_or_404(model, user=request.user,
                                   recipe=recipe)
        follow.delete()
        return Response(
            'Рецепт успешно удален из избранного/списка покупок',
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(
        {'errors': 'Данного рецепта не было в избранном/списке покупок'},
        status=status.HTTP_400_BAD_REQUEST
    )


if __name__ == "__main__":
    insert_into_base_ingredients()
