FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    APP_SQLITE_PATH=/data/noco.db

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip

# Если позже появится requirements.txt, можно заменить на:
# RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "app.ui_cli"]

