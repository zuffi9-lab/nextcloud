@echo off
setlocal

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Python не найден. Установите Python 3.11+ и повторите.
  exit /b 1
)

if not exist .venv (
  python -m venv .venv
)

call .venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
  echo Не удалось активировать виртуальное окружение.
  exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
  echo Не удалось установить зависимости.
  exit /b 1
)

if not exist data mkdir data
if not exist data\config.json copy config.example.json data\config.json >nul

set CONFIG_PATH=data\config.json
set PORT=8080
set RUN_ON_START=true
set SCHEDULE_CRON=0 8 * * *
if "%FLASK_SECRET%"=="" set FLASK_SECRET=change-me

echo Запуск web UI без Docker...
python web_ui.py
