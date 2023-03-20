import json

import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import Error
from contextlib import closing

load_dotenv()


try:
    with closing(psycopg2.connect(
        dbname='postgres',
        user="postgres",
        password='Semafor2003',
        host='localhost',
        port=5432
    )) as conn:
        with conn.cursor() as cursor:
            with open('./../../../data/ingredients.json', 'r', encoding='utf8') as json_file:
                data = json.load(json_file)
                for line in data:
                    title = line.get('name')
                    measurement_unit = line.get('measurement_unit')
                    amount = 0
                    cursor.execute(f"INSERT INTO recipes_ingredientsmodel(title, amount, measurement_unit) VALUES ('{title}', '{amount}', '{measurement_unit}');")
                    conn.commit()

                for i in cursor:
                    print(i)
    print("Соединение с PostgreSQL закрыто")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)


