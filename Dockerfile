# Use an official Python runtime as a parent image
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies and Poetry in one step to minimize layers
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    pip install --upgrade pip && \
    pip install poetry && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the project files into the container
COPY . /app

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Collect static files
RUN poetry run python manage.py collectstatic --noinput

# Use a smaller base image for the runtime environment
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy installed dependencies and project files from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "your_django_project.wsgi:application"]
