# Use the official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Make and apply migrations
RUN python manage.py makemigrations && python manage.py migrate

# Expose the ports
EXPOSE 8000 8001

# Default command to run Gunicorn for HTTP requests.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application", "--timeout", "15", "--preload"]
