# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set environment variables (using proper format to avoid warnings)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install project dependencies
RUN pipenv lock --pre -r > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "savannah.wsgi:application"]
