# Start from a pre-built Python image with uv
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    APP_HOME=/app

# Set the working directory
WORKDIR $APP_HOME

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Create directories for static and media files
RUN mkdir $APP_HOME/static && mkdir $APP_HOME/media && mkdir $APP_HOME/db

# Copy the entire application
COPY . .

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e .

# Change ownership of the directories
RUN chown -R app:app $APP_HOME

# Switch to the non-root user
USER app

# Expose port
EXPOSE 8000

# The command is specified in the docker-compose.yml
# CMD ["gunicorn", "alma.wsgi:application", "--bind", "0.0.0.0:8000"]
