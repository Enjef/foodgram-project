![example workflow](https://github.com/enjef/foodgram-project/actions/workflows/yamdb_workflow.yml/badge.svg)
# Проект: foodgram-project
foodgram-project

### Описание
После выполнения установки в трёх docker-контейнерах(nginx, PostgreSQL и Django) будет развёрнут проект foodgram .
Проект foodgram собирает рецепты авторов. 
Пользователи могут подписываться на рецепты и авторов, создавать свои рецепты, добавлять рецепты в список покупок и распечатывать список необходимых ингредиентов.

В этом проекте настроен Continuous Integration и Continuous Deployment для YaMDB, при пуше в репозиторий происходит:

- автоматический запуск тестов
- обновление образов на Docker Hub
- автоматический деплой на боевой сервер
- отправка уведомления в Telegram

### Технологии
- Python 3.8.5
- django 3.0.5
- docker-compose 3.8
- postgres:12.4

### Запуск проекта
Выполните команды:
```
docker-compose up -d --build
docker-compose exec web python manage.py makemigrations api --noinput
docker-compose exec web python manage.py migrate --noinput
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py loaddata ingredients.json
docker-compose exec web python manage.py createsuperuser
```
### DockerHub
Образ foodgram-project доступен на DockerHub: foodgram-project/yamdb:v1

### Переменные окружения

| Переменная | Описание |
| ------ | ------ |
| DB_NAME | имя базы данных |
| POSTGRES_USER | логин для подключения к базе данных |
| POSTGRES_PASSWORD | пароль для подключения к БД |
| DB_HOST | название сервиса (контейнера) |
| DB_PORT | порт для подключения к БД |


### Github Actions secrets для CI/CD

| Secret | Описание | 
| ------ | ------ |
| DOCKER_USERNAME | пароль DockerHub |
| DOCKER_PASSWORD | логин DockerHub |
| HOST | IP-адрес сервера |
| USER | имя пользователя для подключения к серверу |
| PASSPHRASE | имя пользователя для подключения к серверу |
| SSH_KEY | RSA PRIVATE KEY |
| TELEGRAM_TO | ID телеграм-аккаунта для получения сообщений |
| TELEGRAM_TOKEN | токен телеграм-бота для отправки сообщений |
