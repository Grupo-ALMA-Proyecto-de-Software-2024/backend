# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire application 
COPY . .

# Install requirements directly
RUN pip install django==5.0.3 \
    djangorestframework==3.15.1 \
    drf-spectacular==0.27.2 \
    pillow==10.3.0 \
    django-cors-headers==4.3.1 \
    markdown==3.6 \
    pandas==2.2.2 \
    python-dotenv==1.0.1 \
    django-environ==0.11.2 \
    gunicorn==22.0.0

EXPOSE 8000

# Use a direct command instead of an entrypoint script
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn alma.wsgi:application --bind 0.0.0.0:8000 --workers 3"]

