## Проект: api_yamdb

![Status of workflow runs triggered by the push event](https://github.com/innis8/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

Авторы:
- matsabaleuski
- Innis8
- Serge561

## Описание

Проект YaMDb, а также REST API сервис для него.
Приложение позволяет:
- Добавлять новые произведения в базу данных. 
- Присваивать произведениям категорию и жанры и просматривать их.
- Оставлять отзывы к произведению.
- Оставлять комментарии к отзывам.

Часть сервисов доступна только после авторизации по JWT-токену.

***
#### Предстартовые настройки
Файл переменных окружения infra/.env_example нужно переименовать в .env и поместить туда необходимую информацию:
- секретный ключ Django SECTRET_KEY, использующийся для хеширования и криптографических подписей. Сгенерировать свой ключ можно, например, на сайте https://djecrety.ir/ либо выполнив в терминале команду:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
- информацию относительно PostgreSQL DB

- список разрешенных хостов в виде host_1,host_2,host_n (через запятую, без пробелов)

- разместить настроенный файл infra/.env на удаленный сервер в home/<ваш_username>/.env

- скопировать файлы infra_sp2/docker-compose.yaml и infra_sp2/nginx/default.conf из проекта на удаленный сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно

***
### Запуск проекта в Docker

Клонировать репозиторий:

```
git clone https://github.com/Innis8/yamdb_final.git

```

Перейти в директорию infra и выполнить команду:

```
cd yamdb_final/infra
docker-compose up -d --build
```

Выполнить по очереди команды для создания миграций, создания суперюзера и сбора статики:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

Проект будет доступен по адресу: http://localhost/
Админка по адресу: http://localhost/admin/
Общая документация по адресу: http://localhost/redoc/

В качестве примера рядом с manage.py лежит дамп БД с несколькими тестовыми записями.  
Импортировать дамп в свежесозданную БД можно командой:


```
docker-compose exec web python manage.py loaddata fixtures.json

```

***
### Остановка Docker

Для остановки контейнеров без их удаления выполнить команду:

```
docker-compose stop
```

Для остановки с удалением контейнеров и внутренних сетей, связанных с этими сервисами:

```
docker-compose down
```

Для остановки с удалением контейнеров, внутренних сетей, связанных с этими сервисами, и томов:

```
docker-compose down -v
```

***
### Запуск проекта Docker, после его остановки

Для запуска ранее остановленного проекта, если контейнеры не были удалены:

```
docker-compose start -d
```

Для запуска ранее остановленного проекта, если контейнеры были удалены, но тома - нет:

```
docker-compose up -d
```

***
### Возможности приложения:

***
### Сервис AUTH

Регистрация пользователей и выдача токенов

1. Регистрация нового пользователя

Получить код подтверждения на переданный email.

Права доступа: Доступно без токена.

Использовать имя 'me' в качестве username запрещено.

Поля email и username должны быть уникальными.

Запрос:
```
 POST /api/v1/auth/signup/
```
```
{
  "email": "string",
  "username": "string"
}
```

Ответ:
```
{
  "email": "string",
  "username": "string"
}
```


2. Получение JWT-токена

Получение JWT-токена в обмен на username и confirmation code.

Права доступа: Доступно без токена.

Запрос:
```
POST /api/v1/auth/token/
```
```
{
  "username": "string",
  "confirmation_code": "string"
}
```

Ответ:
```
{
  "token": "string"
}
```

***
### Сервис CATEGORIES

Категории (типы) произведений

1. Получение списка всех категорий

Получить список всех категорий

Права доступа: Доступно без токена

Запрос:
```
 GET /api/v1/categories/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```


2. Добавление новой категории

Создать категорию.

Права доступа: Администратор.

Поле slug каждой категории должно быть уникальным.

Запрос:
```
POST /api/v1/categories/
```
```
{
  "name": "string",
  "slug": "string"
}
```

Ответ:
```
{
  "name": "string",
  "slug": "string"
}
```


3. Удаление категории

Удалить категорию.

Права доступа: Администратор.

Запрос:
```
 DELETE /api/v1/categories/{slug}/
```

***
### Сервис GENRES

Категории жанров

1. Получение списка всех жанров

Получить список всех жанров.

Права доступа: Доступно без токена

Запрос:
```
 GET /api/v1/genres/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```


2. Добавление жанра

Добавить жанр.

Права доступа: Администратор.

Поле slug каждого жанра должно быть уникальным.

Запрос:
```
POST /api/v1/genres/
```
```
{
  "name": "string",
  "slug": "string"
}
```

Ответ:
```
{
  "name": "string",
  "slug": "string"
}
```


3. Удаление жанра

Удалить жанр.

Права доступа: Администратор.

Запрос:
```
 DELETE /api/v1/genres/{slug}/
```

***
### Сервис TITLES

Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

1. Получение списка всех произведений

Получить список всех объектов.

Права доступа: Доступно без токена

Запрос:
```
 GET /api/v1/titles/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```


2. Добавление произведения

Добавить новое произведение.

Права доступа: Администратор.

Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).

При добавлении нового произведения требуется указать уже существующие категорию и жанр.

Запрос:
```
 POST /api/v1/titles/
```
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


3. Получение информации о произведении

Информация о произведении

Права доступа: Доступно без токена

Запрос:
```
 GET /api/v1/titles/{titles_id}/
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


4. Частичное обновление информации о произведении

Обновить информацию о произведении

Права доступа: Администратор

Запрос:
```
PATCH /api/v1/titles/{titles_id}/
```
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


5. Удаление произведения

Удалить произведение.

Права доступа: Администратор.

Запрос:
```
 DELETE /api/v1/titles/{titles_id}/
```


***
### Сервис REVIEWS

Отзывы

1. Получение списка всех отзывов

Получить список всех отзывов.

Права доступа: Доступно без токена.

Запрос:
```
 GET /api/v1/titles/{title_id}/reviews/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```


2. Добавление нового отзыва

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.

Права доступа: Аутентифицированные пользователи.

Запрос:
```
 POST /api/v1/titles/{title_id}/reviews/
```
```
{
  "text": "string",
  "score": 1
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


3. Полуение отзыва по id

Получить отзыв по id для указанного произведения.

Права доступа: Доступно без токена.

Запрос:
```
 GET /api/v1/titles/{title_id}/reviews/{review_id}/
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


4. Частичное обновление отзыва по id

Частично обновить отзыв по id.

Права доступа: Автор отзыва, модератор или администратор.

Запрос:
```
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/
```
```
{
  "text": "string",
  "score": 1
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


5. Удаление отзыва по id

Удалить отзыв по id

Права доступа: Автор отзыва, модератор или администратор.

Запрос:
```
 DELETE /api/v1/titles/{title_id}/reviews/{review_id}/
```

***
### Сервис COMMENTS

Комментарии к отзывам

1. Получение списка всех комментариев к отзыву

Получить список всех комментариев к отзыву по id

Права доступа: Доступно без токена.

Запрос:
```
 GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```


2. Добавление комментария к отзыву

Добавить новый комментарий для отзыва.

Права доступа: Аутентифицированные пользователи.

Запрос:
```
 POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
{
  "text": "string"
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


3. Получение комментария к отзыву

Получить комментарий для отзыва по id.

Права доступа: Доступно без токена.

Запрос:
```
 GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


4. Частичное обновление комментария к отзыву

Частично обновить комментарий к отзыву по id.

Права доступа: Автор комментария, модератор или администратор.

Запрос:
```
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
```
{
  "text": "string"
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


5. Удаление комментария к отзыву

Удалить комментарий к отзыву по id.

Права доступа: Автор комментария, модератор или администратор.

Запрос:
```
 DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```


***
### Сервис USERS

Пользователи

1. Получение списка всех пользователей

Получить список всех пользователей.

Права доступа: Администратор

Запрос:
```
 GET /api/v1/users/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```


2. Добавление пользователя

Добавить нового пользователя.

Права доступа: Администратор

Поля email и username должны быть уникальными.

Запрос:
```
 POST /api/v1/users/
```
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


3. Получение пользователя по username

Получить пользователя по username.

Права доступа: Администратор

Запрос:
```
 GET /api/v1/users/{username}/
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


4. Изменение данных пользователя по username

Изменить данные пользователя по username.

Права доступа: Администратор.

Поля email и username должны быть уникальными.

Запрос:
```
PATCH /api/v1/users/{username}/
```
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


5. Удаление пользователя по username

Удалить пользователя по username.

Права доступа: Администратор.

Запрос:
```
 DELETE /api/v1/users/{username}/
```
