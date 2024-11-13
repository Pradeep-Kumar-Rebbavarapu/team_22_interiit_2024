# Use the official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Collect the Django static files
RUN python manage.py collectstatic --noinput

# Expose the ports
EXPOSE 8000 8001

# Start the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application", "--timeout", "15", "--preload"]