# Проектное задание: Blogicum
## Технологии
- Django 3.2.16 (CBV - представления на основе классов)
- Python 3.10.12
- SQLite 3

## Цепочка проектов Blogicum
[django_sprint1](https://github.com/vasiliy-muravev/django_sprint1 "django_sprint1")

[django_sprint3](https://github.com/vasiliy-muravev/django_sprint3 "django_sprint3")

**[django_sprint4](https://github.com/vasiliy-muravev/django_sprint4 "django_sprint4")** &#8592; вы тут

## Инструкция по запуску проекта (Linux)
**1. Клонирование с Github.**

В локальную директорию клонируйте проект
```
git clone git@github.com:vasiliy-muravev/django_sprint4.git
```
**2. Создание окружения.**

В корневой папке проекта создайте и активируйте виртуальное окружение
```
python3 -m venv venv
source venv/bin/activate
```

**3. Обновление pip и установка зависимостей.**
 
Находясь в корневой папке проекта, выполните команду
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**4. Миграции и загрузка фикстур.**
 
Находясь в папке Django-проекта blogicum, выполните команды
```
python manage.py migrate
python manage.py loaddata db.json
```

**5. Запуск проекта.**
 
Находясь в папке Django-проекта blogicum, выполните команду
```
python3 manage.py runserver
```

**6. Создание суперпользователя.**
 
Находясь в папке Django-проекта blogicum, выполните команду createsuperuser и задайте имя пользователя и пароль (например admin1 и admin)
```
python manage.py createsuperuser
```


Перейдите на http://127.0.0.1:8000/admin и войдите в админку с заданными реквизитами

## Полезные команды
После каждого изменения в модели blog/models.py необходимо создавать и применять миграции чтобы произошли изменения в БД
```
python manage.py makemigrations
python manage.py migrate
```