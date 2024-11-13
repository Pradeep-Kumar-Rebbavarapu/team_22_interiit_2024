# Use the official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000 8001

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application", "--timeout", "15", "--preload"]
