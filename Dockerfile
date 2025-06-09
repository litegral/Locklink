FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.docker.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.docker.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/db

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

CMD ["sh", "/app/entrypoint.sh"] 