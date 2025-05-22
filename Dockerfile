# Start from a pre-built Python image with uv
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire application
COPY . .

# Install dependencies with uv (using system Python for containers)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e .

# Expose port
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn alma.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
