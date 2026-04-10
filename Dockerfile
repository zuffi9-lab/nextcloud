FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY nextcloud_fn_ofd_reminder.py web_ui.py config.example.json ./
COPY templates ./templates

ENV CONFIG_PATH=/data/config.json
ENV PORT=8080

VOLUME ["/data"]
EXPOSE 8080

CMD ["python", "web_ui.py"]
