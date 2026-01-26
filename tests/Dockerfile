FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY .. /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements-test.txt

# Set environment for CI/CD (2.0x timeout multiplier)
ENV CI=true
ENV CI_ENVIRONMENT=docker

# Default command runs tests
CMD ["pytest", "tests/", "-v", "--tb=short", "--color=yes"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pytest; print('OK')" || exit 1
