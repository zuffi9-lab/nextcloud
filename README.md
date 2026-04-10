# FN/OFD Reminder для Nextcloud (Docker + web-интерфейс)

Готово для установки **из репозитория**: приложение собирается в Docker-образ и поднимается как сервис с интерфейсом настройки.

## Что делает

- Читает XLSX-файл с диска Nextcloud (WebDAV).
- Создает/обновляет события в календаре Nextcloud (CalDAV) для сроков ФН и ОФД.
- Отправляет уведомления в Telegram:
  - за 30 дней до истечения срока,
  - затем каждые 10 дней,
  - после истечения срока — каждые 10 дней до обновления даты в таблице.

## Быстрый старт

```bash
git clone <repo_url>
cd nextcloud
docker compose up -d --build
```

Откройте интерфейс: `http://localhost:8080`.

## Интерфейс настройки

В web UI доступны поля:
- параметры Nextcloud (`base_url`, `username`, `app_password`, `xlsx_webdav_path`, `calendar_url`),
- Telegram (`bot_token`, `chat_id`),
- путь к SQLite БД,
- названия колонок XLSX,
- timezone,
- кнопка «Запустить сейчас» для ручного запуска.

Конфиг сохраняется в `/data/config.json`.

## Cron-расписание внутри контейнера

Используется встроенный scheduler (APScheduler), задается переменной:

- `SCHEDULE_CRON=0 8 * * *` — запуск ежедневно в 08:00.

## Формат XLSX

По умолчанию ожидаются колонки:
- `id`
- `title`
- `fn_expiry_date`
- `ofd_expiry_date`

Поддерживаемые форматы дат: `YYYY-MM-DD`, `DD.MM.YYYY`, Excel datetime.

## Переменные окружения

- `CONFIG_PATH` (по умолчанию `/data/config.json`)
- `PORT` (по умолчанию `8080`)
- `RUN_ON_START` (`true/false`)
- `SCHEDULE_CRON` (cron-выражение)
- `FLASK_SECRET`

## Локальная разработка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python web_ui.py
```
