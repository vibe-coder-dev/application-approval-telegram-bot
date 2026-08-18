# Dockerfile for Application Bot
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/uploads/photos /app/uploads/documents /app/uploads/files

# Set permissions
RUN chown -R 1000:1000 /app/data /app/uploads

# Switch to non-root user
USER 1000

# Expose ports (bot webhooks + web admin panel)
EXPOSE 8080
EXPOSE 10000

# Set default command
CMD ["python", "-m", "bot.main"]
