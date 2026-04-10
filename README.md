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

## Установка на Ubuntu (Docker)

Проверено для Ubuntu 22.04/24.04.

### 1) Установите Docker Engine + Compose plugin

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu   $(. /etc/os-release && echo $VERSION_CODENAME) stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

### 2) Клонируйте репозиторий и запустите сервис

```bash
git clone <repo_url>
cd nextcloud
docker compose up -d --build
```

### 3) Откройте web-интерфейс

- `http://localhost:8080`

Заполните параметры Nextcloud/Telegram, сохраните и нажмите «Запустить сейчас».


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


## Вариант для TrueNAS SCALE

Добавлен отдельный набор файлов в `truenas/` для установки через Custom App:

- `truenas/docker-compose.truenas.yml`
- `truenas/.env.example`
- `truenas/README.md`

Подробная инструкция: `truenas/README.md`.


## Публикация репозитория для TrueNAS

Добавлен отдельный гайд по публикации на GitHub + автоматической публикации образа в GHCR:

- `PUBLISH_TRUENAS.md`
- `.github/workflows/publish-ghcr.yml`
