# Продуктовый помощник - Foodgram
### URL

Проект развернут на сайте: .......

### Описание проекта:

Сайт разработан для тех, кто любит готовить и готов делиться своими рецептами . После регистрации, дорогой друг, ты сможешь публиковать свой рецепт, а так же подписываться на других авторов, добавлять их рецепты в избранное, а так же скачивать список ингредиентов, для покупки их в супермаркете , ведь они так необходимы для приготовления какого - либо блюда!

### *Технологии, которые использовались:*
<div>
<img src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/python/python-original.svg" title="Python" alt="Python" width="90" height="90"/>&nbsp;
<img src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/docker/docker-original-wordmark.svg" title="docker"  alt="django" width="90" height="90"/>&nbsp;
<img src="https://icongr.am/devicon/javascript-original.svg?size=138&color=currentColor
" title="django"  alt="django" width="90" height="90"/>&nbsp;
<img src="https://icongr.am/devicon/linux-original.svg?size=138&color=currentColor
" title="django"  alt="django" width="90" height="90"/>&nbsp;
<img src="https://icongr.am/devicon/postgresql-original-wordmark.svg?size=138&color=currentColor
" title="django"  alt="django" width="90" height="90"/>&nbsp;
<img src="https://icongr.am/devicon/react-original-wordmark.svg?size=138&color=currentColor
" title="django"  alt="django" width="90" height="90"/>&nbsp;
<img src="https://raw.githubusercontent.com/devicons/devicon/1119b9f84c0290e0f0b38982099a2bd027a48bf1/icons/django/django-plain-wordmark.svg" title="django"  alt="django" width="90" height="90"/>&nbsp;
<img src="https://www.vectorlogo.zone/logos/gunicorn/gunicorn-ar21.svg" title="django"  alt="django" width="" height="90"/>&nbsp;
<img src="https://www.vectorlogo.zone/logos/nginx/nginx-ar21.svg" title="django"  alt="django" width="" height="90"/>&nbsp;
<img src="https://timeweb.com/ru/community/article/0c/0c82a1f92cfa7d43060a88ab5bd73f3d.png" title="django"  alt="django" width="" height="120"/>&nbsp;
</dev>

### Запуск проекта в dev-режиме:

-   Клонируйте репозиторий и перейдите в него в командной строке:

```
git@github.com:Efesov/foodgram-project-react.git

```

```
cd foodgram-project-react

```

-   Запустите проект с помощью команды:

```
docker compose up

```

-   Соберите статику Django с помощью команды:

```
docker compose exec backend python manage.py collectstatic

```

-   Скопируйте статику командой:

```
docker compose exec backend cp -r /app/collected_static/. /static/static/
