# Use the official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8088 8001

CMD ["gunicorn", "--bind", "0.0.0.0:8088", "backend.wsgi:application", "--timeout", "15", "--preload"]
