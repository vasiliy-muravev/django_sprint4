# Проектное задание: Blogicum
## Инструкция по запуску проекта
**1. Клонирование с Github.**

В рабочей директории с проектами запустить
```
git clone git@github.com:vasiliy-muravev/django_sprint4.git
```
**2. Создание окружения.**

В корневой папке проекта создайте виртуальное окружение, используя команду
```
python3 -m venv venv
```
Активируйте виртуальное окружение командой
```
source venv/bin/activate
```

**3. Установка зависимостей.**
 
Находясь в корневой папке проекта, выполните команду
```
pip install requirements.txt
```

**4. Запуск проекта.**
 
Находясь в папке Django-проекта blogicum, выполните команду
```
python3 manage.py runserver
```

**5. Миграции и загрузка фикстур.**
 
Находясь в папке Django-проекта blogicum, выполните команды
```
python manage.py migrate
python manage.py loaddata ./../db.json
```

**6. Создание суперпользователя.**
 
Находясь в папке Django-проекта blogicum, выполните команду createsuperuser и задайте имя пользователя и пароль (например admin1 и admin)
```
python manage.py createsuperuser
```


Перейдите на http://127.0.0.1:8000/admin и войдите в админку с заданными реквизитами

### Полезные команды
После каждого изменения в модели blog/models.py необходимо создавать и применять миграции чтобы произошли изменения в БД
```
python manage.py makemigrations
python manage.py migrate
```