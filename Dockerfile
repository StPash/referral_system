FROM python:3.12-slim AS builder

WORKDIR app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "referral_system.wsgi:application", "--bind", "0.0.0.0:8000"]