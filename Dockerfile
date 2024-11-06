# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl make && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && mv /root/.local/bin/poetry /usr/local/bin/
RUN poetry --version

# Disable Poetry's virtual environment creation
ENV POETRY_VIRTUALENVS_CREATE=false

# RUN poetry config virtualenvs.create true && \
#     poetry config virtualenvs.in-project true && \
#     poetry config virtualenvs.path "/app/.venv"

# Install project dependencies
RUN poetry install --no-root --no-cache

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

