#!/usr/bin/env python3
import json
import os
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for, flash
from apscheduler.schedulers.background import BackgroundScheduler

from nextcloud_fn_ofd_reminder import read_config, process

CONFIG_PATH = Path(os.getenv("CONFIG_PATH", "config.json"))
RUN_ON_START = os.getenv("RUN_ON_START", "true").lower() == "true"
SCHEDULE_CRON = os.getenv("SCHEDULE_CRON", "0 8 * * *")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change-me")
scheduler = BackgroundScheduler()


def default_config():
    return {
        "nextcloud": {
            "base_url": "https://cloud.example.com",
            "username": "user",
            "app_password": "app-password",
            "xlsx_webdav_path": "/remote.php/dav/files/user/Finance/fn_ofd.xlsx",
            "calendar_url": "https://cloud.example.com/remote.php/dav/calendars/user/finance/",
        },
        "telegram": {
            "bot_token": "",
            "chat_id": "",
        },
        "database": {
            "path": "state.db",
        },
        "columns": {
            "id": "id",
            "title": "title",
            "fn_expiry_date": "fn_expiry_date",
            "ofd_expiry_date": "ofd_expiry_date",
        },
        "event": {
            "timezone": "Europe/Moscow",
        },
    }


def load_or_default():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    cfg = default_config()
    save_config(cfg)
    return cfg


def save_config(cfg):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def run_job():
    cfg = read_config(str(CONFIG_PATH))
    process(cfg)


def schedule_job():
    minute, hour, day, month, dow = SCHEDULE_CRON.split()
    scheduler.add_job(
        run_job,
        trigger="cron",
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=dow,
        id="fn_ofd_job",
        replace_existing=True,
    )
    scheduler.start()


@app.route("/")
def index():
    cfg = load_or_default()
    return render_template("settings.html", cfg=cfg, cron=SCHEDULE_CRON)


@app.route("/save", methods=["POST"])
def save():
    cfg = {
        "nextcloud": {
            "base_url": request.form.get("base_url", "").strip(),
            "username": request.form.get("username", "").strip(),
            "app_password": request.form.get("app_password", "").strip(),
            "xlsx_webdav_path": request.form.get("xlsx_webdav_path", "").strip(),
            "calendar_url": request.form.get("calendar_url", "").strip(),
        },
        "telegram": {
            "bot_token": request.form.get("bot_token", "").strip(),
            "chat_id": request.form.get("chat_id", "").strip(),
        },
        "database": {
            "path": request.form.get("db_path", "state.db").strip(),
        },
        "columns": {
            "id": request.form.get("col_id", "id").strip(),
            "title": request.form.get("col_title", "title").strip(),
            "fn_expiry_date": request.form.get("col_fn", "fn_expiry_date").strip(),
            "ofd_expiry_date": request.form.get("col_ofd", "ofd_expiry_date").strip(),
        },
        "event": {
            "timezone": request.form.get("timezone", "Europe/Moscow").strip(),
        },
    }
    save_config(cfg)
    flash("Конфигурация сохранена")
    return redirect(url_for("index"))


@app.route("/run", methods=["POST"])
def run_now():
    try:
        run_job()
        flash("Задача выполнена успешно")
    except Exception as exc:
        flash(f"Ошибка выполнения: {exc}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    load_or_default()
    schedule_job()
    if RUN_ON_START:
        try:
            run_job()
        except Exception:
            pass
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
