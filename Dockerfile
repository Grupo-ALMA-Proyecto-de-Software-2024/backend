# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies and uv
RUN apt-get update && \
    apt-get install -y curl make gcc && \
    rm -rf /var/lib/apt/lists/* && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

# Optional: Add uv to PATH explicitly (if needed)
ENV PATH="/root/.cargo/bin:$PATH"

# Pre-install dependencies using uv
RUN uv sync --all-extras --dev

# Copy and set up the entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
