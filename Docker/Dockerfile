FROM python:3.13-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files from root to container
# Note: This Dockerfile is intended to be built from the project root:
# docker build -t subdominator -f Docker/Dockerfile .
COPY . .

# Install dependencies and the package globally in the container
RUN uv pip install --no-cache .

# Set the entrypoint to the subdominator CLI
ENTRYPOINT ["subdominator"]
