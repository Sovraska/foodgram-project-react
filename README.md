# Foodrgam

 Продуктовый помощник - дипломный проект курса на Яндекс.Практикум.
 Это онлайн-сервис и API для него. 

 Здесь пользователи могут публиковать рецепты,

 подписываться на публикации других пользователей,

 перед походом в магазин скачивать Можно будет список продуктов :grinning:

## О проекте 

- Проект завернут в Docker-контейнерах;
- Проект был развернут на сервере: <http://51.250.100.232/>
- <http://51.250.100.232/admin>
  - login: admin
  - password: 123

## Развертывание проекта

1. Установите на сервере `docker` и `docker-compose`
2. Создайте файл `/infra/.env` Шаблон для заполнения файла нахоится в `/infra/.env.example`
3. Из директории `/infra/` выполните команду `docker-compose up -d --buld`
4. Создайте миграции `docker-compose exec app python manage.py makemigrations`
5. Выполните миграции `docker-compose exec app python manage.py migrate`
6. Создайте суперюзера `docker-compose exec app python manage.py createsuperuser`
7. Соберите статику `docker-compose exec app python manage.py collectstatic --no-input`
8. Заполните базу ингредиентами `docker-compose exec app python api/utils.py`
9. **Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.**
10. Документация к API находится по адресу: <http://51.250.100.232/api/docs/>.

## Автор

- [Семён Новиков](https://github.com/Sovraska) 
