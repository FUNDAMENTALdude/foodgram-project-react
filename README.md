# Контейнер с foodgram-project-react и его workflow

## Описание
Foodgram это «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Бейдж
![badge status](https://github.com/FUNDAMENTALdude/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push)

## Технологии
Django, Python, Docker, Workflow, JS
 
## Автор
FUNDAMENTALdude

### Шаблон заполнения .env файла
```
DB_ENGINE=
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/FUNDAMENTALdude/foodgram-project-react.git
```

Собрать контейнер
```
cd infra
sudo docker-compose up -d --build
```

Выполнить миграции:
```
sudo docker-compose exec backend python manage.py migrate

```

Собрать статику:
```
docker-compose exec backend python manage.py collectstatic --no-input 
```


### Проект работает по адресу(на удаленном сервере)
http://51.250.90.30/
