# Продуктовый помощник - Foodgram
### URL
Проект развернут на сайте: https://groceryassistant.sytes.net
Учётные данные для входа от Администратора:
Login: `aefesov@yandex.ru`
Password: `master72`
### Описание проекта:
Сайт разработан для тех, кто любит готовить и готов делиться своими рецептами . После регистрации, дорогой друг, ты сможешь публиковать свой рецепт, а так же подписываться на других авторов, добавлять их рецепты в избранное, а так же скачивать список ингредиентов, для покупки их в супермаркете , ведь они так необходимы для приготовления какого - либо блюда!
### *Технологии, которые использовались:*
<div>
<img  src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/python/python-original.svg"  title="Python"  alt="Python"  width="90"  height="90"/>&nbsp;
<img  src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/docker/docker-original-wordmark.svg"  title="docker"  alt="django"  width="90"  height="90"/>&nbsp;
<img  src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/javascript/javascript-original.svg"  title="django"  alt="django"  width="90"  height=""/>&nbsp;
<img  src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/linux/linux-original.svg"  title="django"  alt="django"  width="90"  height=""/>&nbsp;
<img  src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/postgresql/postgresql-original-wordmark.svg"  title="django"  alt="django"  width="90"  height=""/>&nbsp;
<img  src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/react/react-original-wordmark.svg"  title="django"  alt="django"  width="90"  height=""/>&nbsp;
<img  src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/django/django-plain-wordmark.svg"  title="django"  alt="django"  width="90"  height="90"/>&nbsp;
<img  src="https://www.vectorlogo.zone/logos/gunicorn/gunicorn-ar21.svg"  title="django"  alt="django"  width=""  height="90"/>&nbsp;
<img  src="https://www.vectorlogo.zone/logos/nginx/nginx-ar21.svg"  title="django"  alt="django"  width=""  height="90"/>&nbsp;
<img src="https://timeweb.com/ru/community/article/0c/0c82a1f92cfa7d43060a88ab5bd73f3d.png"  title="django"  alt="django"  width=""  height="120"/>&nbsp;
</dev>

### Запуск проекта в dev-режиме:

- #### Клонируйте репозиторий и перейдите в него в командной строке:
```git@github.com:Efesov/foodgram-project-react.git```
```cd foodgram-project-react```
- #### Cоздать и активировать виртуальное окружение: 
-  - ##### На Mac & Linux: `python3 -m venv env`/ `source env/bin/activate`
-  - ##### На Windows: `python -m venv venv` / `source venv/Scripts/activate`
- #### Установить зависимости из файла requirements.txt:
-  - ##### На Mac & Linux: `python3 -m pip install --upgrade pip` / `pip install -r requirements.txt`
-  - ##### На Windows: `python -m pip install --upgrade pip` / `pip install -r requirements.txt`

- #### Переходим в директорию `/infra/` и создаем там файл `.env` с содержанием:
``
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
SECRET_KEY=<секретный ключ проекта django>``



- - #### Запускаем docker-compose.yml
`docker-compose up --build`

## Если вы хотите запустить сервер удалённо, то

-   #### Выполните вход на свой удаленный сервер
    
-   #### Установите docker на сервер:
```sudo apt install docker.io ```
-   #### Установите docker-compose на сервер:
``sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose``

-  #### Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
-   #### Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:

```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```
-  ### Cоздайте .env файл и впишите:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>    
    ```
-   ### Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
    
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
    
    SECRET_KEY=<секретный ключ проекта django>
    
    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
    
    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    
    ```
  ### Workflow состоит из трёх шагов:
    
    -   Проверка кода на соответствие PEP8
    -   Сборка и публикация образа бекенда на DockerHub.
    -   Автоматический деплой на удаленный сервер.
    -   Отправка уведомления в телеграм-чат.

-  #### На сервере соберите docker-compose:
   
```
sudo docker-compose up -d --build

```

-  #### После успешной сборки на сервере выполните команды (только после первого деплоя):
    
    - ####  Соберите статические файлы:
    
    ```
    sudo docker-compose exec backend python manage.py collectstatic
   
    ```
    
    -  #### Примените миграции:
    
    ```
    sudo docker-compose exec backend python manage.py makemigrations
        
    sudo docker-compose exec backend python manage.py migrate 
    
    ```
    
    -   #### Загрузите ингридиенты в базу данных (необязательно):  
        - ##### Если файл не указывать, по умолчанию выберется ingredients.json_
    ```
    sudo docker-compose exec backend python manage.py <Название файла из директории data>
    
    ```
    
    - ####  Создаем Суперпользователя Django:
    
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    
    ```
    
      ## Проект доступен по вашему IP .

## Бэкенд подготовил:
[Efesov](https://github.com/Efesov)