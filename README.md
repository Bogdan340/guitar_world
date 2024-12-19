## Ссылки
![GitHub](https://github.com/Bogdan340/guitar_world)

# Запуск проекта без docker

1. Клонирование проекта с github
```git clone https://github.com/Bogdan340/guitar_world.git```
2. Переход в директорию проекта

```cd guitar_world```

3. Создание виртуального окружения

```python3 -m venv venv```

4. Активация виртуального окружения

```./.venv/Scripts/activate```

5. Переход в директорию проекта django

```cd guitar_world```

6. Установка зависимостей

```pip install -r requirements.txt```

7. Замена настроек базы данных

```Задите в settings и раскоментируйте код отвечающий за подключения sqlite базы данных, и закоментируйте код отвечающий за подключение postgresql базы данных```

8. Запуск проекта

```python manage.py runserver```

# Запуск проекта с docker

1. Клонирование проекта с github

```git clone https://github.com/Bogdan340/guitar_world.git```
2. Переход в директорию проекта

```cd guitar_world```

3. Сборка и запуск проекта

```docker-compose up --build```

4. Создание супер пользователя

```Зайдите в docker desktop перейдите в вкладку 'Containers', найдите проект guitar_world, нажмите на три точки, после нажмите на 'View details'. Где написано guitar_world-web-1 нажмите на трое точие и выберете 'Open in terminal', после чего в открывшемся терминале введите 'python manage.py createsuperuser', введите данные супер пользователя.```
