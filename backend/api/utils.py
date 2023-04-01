import json
import os
from contextlib import closing
from pathlib import Path

import psycopg2
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from psycopg2 import Error
import logging

from rest_framework import status
from rest_framework.response import Response

from recipes.models import RecipesModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(os.path.join(BASE_DIR / 'infra', '.env'))

DB_NAME = str(os.getenv('DB_NAME'))
POSTGRES_USER = str(os.getenv('POSTGRES_USER'))
POSTGRES_PASSWORD = str(os.getenv('POSTGRES_PASSWORD'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_PORT = str(os.getenv('DB_PORT'))


def insert_into_base_ingredients():
    try:
        with closing(psycopg2.connect(
                dbname=DB_NAME,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
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
        logging.info("Соединение с PostgreSQL закрыто")

    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL", error)


def delete_obj(request, pk, model):
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


def post_obj(request, pk, model, serializer):
    recipe = get_object_or_404(RecipesModel, pk=pk)
    if model.objects.filter(user=request.user, recipe=recipe).exists():
        return Response(
            {'errors': 'Рецепт уже есть в избранном/списке покупок'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    model.objects.get_or_create(user=request.user, recipe=recipe)
    data = serializer(recipe).data
    return Response(data, status=status.HTTP_201_CREATED)


if __name__ == "__main__":
    insert_into_base_ingredients()
