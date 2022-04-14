# api_yamdb

### Разработчики:

 - Шепилов Алексей (https://github.com/FoorsAlex)
 - Мирошниченко Евгений (https://github.com/Eugenii1996)
 - Владимир Ветров (https://github.com/VSVetrov)

### О проекте:

Проект YaMDb представляет собой платформу по сбору отзывов пользователей на опубликованные произведения.
Предоставляет клиентам доступ к базе данных.
Данные передаются в формате JSON.
В реализации проекта применена архитектура REST API.
Примененные библиотеки:
 - requests 2.26.0
 - django 2.2.16
 - djangorestframework 3.12.4
 - PyJWT 2.1.0
 - pytest 6.2.4
 - pytest-django 4.4.0
 - pytest-pythonpath 0.7.3
 - djangorestframework_simplejwt 5.1.0
 - django-filter 21.1

### Как наполнить базу данных:

Для Windows:
 1. Запустить sqlite3.exe
 2. Открыть базу данных командой «.open FILENAME»
 3. Выполнить команду для заполнения конкретной таблицы в базе данных:
    .import --csv --skip 1 C:/work/somedata.csv tab1,
    где  --csv - формат считываемого файла,
    --skip 1 - пропустить первую строку csv файла при импорте,
    C:/work/somedata.csv - путь расположения csv файла,
    tab1 - имя таблицы в базе данных
Порядок столбцов в csv файле должен соответствовать порядку столбцов таблицы в базе данных.

### Как запустить проект на Windows:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Eugenii1996/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3.7 -m venv venv
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Примеры запросов к API:

Описание API доступно по ссылке http://127.0.0.1:8000/redoc/ при запуске сервера разработчика

POST-запрос на эндпоинт api/v1/titles/:

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

GET-запрос на эндпоинт /api/v1/titles/ вернет список произведений:

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
