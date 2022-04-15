# api_yamdb

### Разработчики:

 - [Шепилов Алексей](https://github.com/FoorsAlex)
 - [Мирошниченко Евгений](https://github.com/Eugenii1996)
 - [Владимир Ветров](https://github.com/VSVetrov)

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

Выполнить комманду python manager.py fill_db_from_csv_files <путь файла>

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

Описание API доступно по ссылке http://127.0.0.1:8000/redoc/ при запуске сервера разработчика
