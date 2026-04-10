@echo off
setlocal

where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Docker не найден. Установите Docker Desktop и повторите.
  exit /b 1
)

if not exist data mkdir data

echo Запуск FN/OFD Reminder через docker-compose.windows.yml ...
docker compose -f docker-compose.windows.yml up -d --build
if %ERRORLEVEL% NEQ 0 (
  echo Ошибка запуска контейнера.
  exit /b 1
)

echo Готово. Откройте: http://localhost:8080
