## Проект: api_yamdb

![Status of workflow runs triggered by the push event](https://github.com/innis8/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

## Описание

Проект YaMDb, а также REST API сервис для него.
Приложение позволяет:
- Добавлять новые произведения в базу данных. 
- Присваивать произведениям категорию и жанры и просматривать их.
- Оставлять отзывы к произведению.
- Оставлять комментарии к отзывам.

Часть сервисов доступна только после авторизации по JWT-токену. Смотреть в общей документации по адресу:
`http://<your remote server>/redoc/`


***
## Workflow
Запускается при пуше в ветку `master`, не запускается, если в коммите была лишь правка файла `README.md`

Состоит из следующих шагов:

|Шаг|Что делает|
| - |
| tests | Установка зависимостей, запуск тестов flake8 и pytest |
| build_and_push_to_docker_hub | Сборка образа и отправка в свой репозиторий на DockerHub |
| deploy | Разворачивание проекта на удалённом сервере |
| send_message | Отправка уведомления в телеграм-чат при успешном прохождении workflow в GitHub Actions |

***
### Подготовка и запуск проекта в Docker

Клонировать репозиторий:

```
git clone https://github.com/Innis8/yamdb_final.git

```

***
Файл переменных окружения infra/.env_example нужно переименовать в .env и поместить туда необходимую информацию:
- секретный ключ Django SECTRET_KEY, использующийся для хеширования и криптографических подписей. Сгенерировать свой ключ можно, например, на сайте https://djecrety.ir/ либо выполнив в терминале команду:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
- информацию относительно PostgreSQL DB

- список разрешенных хостов в виде host_1,host_2,host_n (через запятую, без пробелов)

- разместить настроенный файл infra/.env на удаленный сервер в home/<ваш_username>/.env

***
Пример заполнения infra/.env
```
SECRET_KEY=YOUR_SECRET_KEY_FROM_SETTINGS.PY

# ./infra/.env 
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<<<пароль для БД>>>
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=12.0.0.1,localhost,other_hosts(через запятую без пробелов)
```

***
### Установка на удаленном сервере (Ubuntu):
1\. Войти на свой удалённый сервер:

```
ssh <your_login>@<ip_address>
```

2\. Установить Docker на удалённый сервер:

```
sudo apt install docker.io
```

3\. Установить docker-compose на удалённый сервер:
 - Проверить, какая последняя версия доступна на [странице релизов](https://github.com/docker/compose/releases 'https://github.com/docker/compose/releases'). На момент написания настоящего документа наиболее актуальной стабильной версией является v2.10.2
 - Следующая команда загружает версию 1.26.0 и сохраняет исполняемый файл в каталоге `/usr/local/bin/docker-compose`, в результате чего данное программное обеспечение будет глобально доступно под именем `docker-compose`:

```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.10.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

- Затем необходимо задать правильные разрешения, чтобы сделать команду docker-compose исполняемой:

```
sudo chmod +x /usr/local/bin/docker-compose
```

- Чтобы проверить успешность установки, запустить следующую команду:

```
docker-compose --version
```

- Вывод будет выглядеть следующим образом:

```
Docker Compose version v2.10.2
```

4\. Скопировать файлы `infra/.env`, `infra/docker-compose.yaml` и `infra/nginx/default.conf` из проекта на удаленный сервер в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf` соответственно. Сделать это можно при помощи сторонней программы, например, WinSCP, либо выполнив следующую команду из корневой папки проекта:

```
scp infra/.env <username>@<host>:/home/<username>/infra/.env
scp infra/docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp -r infra/nginx/ <username>@<host>:/home/<username>/
```

5\. Добавить переменные окружения в Secrets на GitHub:

```
DOCKER_USERNAME=<<<<<<имя пользователя DockerHub>>>
DOCKER_PASSWORD=<<<пароль DockerHub>>>
USER_YACLOUD=<<<имя пользователя удалённого сервера>>>
HOST_YACLOUD=<<<IP-адрес удалённого сервера>>>
TELEGRAM_TO=<<<ID своего телеграм-аккаунта>>>
TELEGRAM_TOKEN=<<<токен своего бота>>>
SSH_KEY=<<<приватный SSH-ключ, получить можно выполнив команду на локальной машине: cat ~/.ssh/id_rsa>>>
```

***
### После деплоя

Зайти на удалённый сервер и выполнить по очереди команды для создания миграций, создания суперюзера и сбора статики:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

Админка по адресу: `http://<IP-адрес удаленного сервера>/admin/`
Либо, если зарегистрировано доменное имя): `http://<название сайта>/admin/`
Общая документация по адресу: `http://<IP-адрес удаленного сервера>/redoc/`
Либо, если зарегистрировано доменное имя: `http://<название сайта>/redoc/`


***
### Остановка Docker
Если команда не выполняется и в терминале говорится о недостатке прав, вставить перед командой `sudo`
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

***
Авторы:
- matsabaleuski
- Innis8
- Serge561
