# Вариант для TrueNAS SCALE

Ниже — готовый вариант развёртывания сервиса в **TrueNAS SCALE** через **Apps → Discover Apps → Custom App (Docker Compose)**.

## 1) Подготовьте dataset

Создайте dataset, например:
- `/mnt/tank/apps/fn-ofd-reminder/data`

Он будет хранить:
- `config.json` (настройки через UI)
- `state.db` (состояние напоминаний)

## 2) Подготовьте compose и env

Скопируйте файлы из папки `truenas/`:
- `docker-compose.truenas.yml`
- `.env.example` → переименовать в `.env` и задать `FLASK_SECRET`

## 3) Имидж

В `docker-compose.truenas.yml` замените `image` на ваш опубликованный образ, например:
- `ghcr.io/<org>/<repo>:<tag>`

> Для TrueNAS удобнее использовать **готовый registry image**, а не `build: .`.

## 4) Установка в TrueNAS

1. Apps → Discover Apps → **Custom App**.
2. Выберите режим Docker Compose.
3. Вставьте содержимое `docker-compose.truenas.yml`.
4. Добавьте переменные из `.env`.
5. Deploy.

После запуска интерфейс будет доступен на порту `38080`:
- `http://<truenas-ip>:38080`

## 5) Первичная настройка

Через web UI заполните:
- параметры Nextcloud (`base_url`, `username`, `app_password`, `xlsx_webdav_path`, `calendar_url`),
- Telegram (`bot_token`, `chat_id`),
- названия колонок XLSX.

Нажмите **«Сохранить настройки»**, затем **«Запустить сейчас»** для проверки.

## Примечания

- Cron задаётся переменной `SCHEDULE_CRON` (по умолчанию `0 8 * * *`).
- Если используете HTTPS reverse proxy в TrueNAS — пробрасывайте порт 8080 на внутренний сервис.
