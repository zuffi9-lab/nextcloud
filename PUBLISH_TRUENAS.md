# Публикация репозитория для TrueNAS

Этот проект готов к публикации как GitHub-репозиторий с автоматической сборкой Docker-образа в GHCR.

## 1. Опубликуйте репозиторий на GitHub

```bash
git remote add origin git@github.com:<you>/fn-ofd-reminder.git
git branch -M main
git push -u origin main
```

## 2. Включите GitHub Actions

В репозитории уже есть workflow:
- `.github/workflows/publish-ghcr.yml`

Он публикует образ в:
- `ghcr.io/<owner>/fn-ofd-reminder`

Триггеры:
- push в `main`
- push тега `v*`
- ручной запуск `workflow_dispatch`

## 3. Выпустите стабильный тег

```bash
git tag v1.0.0
git push origin v1.0.0
```

После этого TrueNAS сможет тянуть:
- `ghcr.io/<owner>/fn-ofd-reminder:v1.0.0`
- `ghcr.io/<owner>/fn-ofd-reminder:latest`

## 4. Настройте TrueNAS Custom App

1. Откройте `truenas/docker-compose.truenas.yml`.
2. Подставьте ваш owner в image:
   - `ghcr.io/<github_org_or_user>/fn-ofd-reminder:latest`
3. Разверните через **Apps → Discover Apps → Custom App**.

Подробнее: `truenas/README.md`.
