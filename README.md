# foodgram-project

![Workflow Status](https://github.com/PySCBist/foodgram-project/workflows/foodgram%20workflow/badge.svg)

***Foodgram*** - это сайт рецептов. Продуктовый помощник, позволяющий просматривать и создавать рецепты, добавлять их в
избранное, подписываться на авторов рецептов, формировать список покупок с ингредиентами для приготовления понравившихся
блюд.

### Запуск проекта с использованием Docker

Клонируйте репозиторий или скопируйте следующие файлы и папки:

   ```
    nginx/
    docker-compose.yaml
    .env-template
   ```

1. Измените файл `.env-template`
   и переименуйте в `.env`


2. Для запуска проекта выполните:

   `docker-compose up -d`


3. Запускаем терминал внутри контейнера:

   `docker-compose exec app bash`


3. При первом запуске необходимо применить миграции:

   `cd code`  затем `python manage.py migrate`


4. Соберите статику:

   `python manage.py collectstatic`


5. Создайте пользователя с правами администратора:

   `python manage.py createsuperuser`

6. Загрузите фикстуры (ингредиенты и тэги)

   `python manage.py loaddata ingredients.json`
   `python manage.py loaddata tags.json`

Готово!
