# ─── Helpdesk AI — Backend Dockerfile ───────────────
FROM python:3.11-slim

# System deps (build + psql client for healthcheck)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python deps first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

EXPOSE 8000

# Dev command (compose override kar sakta hai)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
