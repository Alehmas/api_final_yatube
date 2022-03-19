## Описание
API для приложения Yatube. 


## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

`git clone https://github.com/Oleg-2006/api_final_yatube`

`cd api_final_yatube`

Cоздать и активировать виртуальное окружение:

`python -m venv env`

`source venv/Scripts/activate`

Установить зависимости из файла requirements.txt:

`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

Выполнить миграции:

`python manage.py migrate`

Запустить проект:

`python manage.py runserver`

## Примеры запросов:

`api/v1/posts/` (POST)создаём новый пост
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
`api/v1/posts/{post_id}/` (GET, PUT, PATCH, DELETE): получаем, редактируем или удаляем пост по id
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
`api/v1/posts/{post_id}/comments/` (POST):создаём новый, указав id поста, который хотим прокомментировать.
```
{
  "text": "string"
}
```
