FROM python:3.10-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app

RUN pip install --upgrade pip --no-cache-dir && pip install psycopg2-binary && pip install -r requirements.txt --no-cache-dir;

COPY . .

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]