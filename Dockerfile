# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.7.1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    mv /root/.local/bin/poetry /usr/local/bin/

# Copy the entire application first
COPY . .

# Install dependencies
RUN poetry install --no-root --no-cache

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Make sure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

