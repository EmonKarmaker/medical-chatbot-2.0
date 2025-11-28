FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements_render.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the sentence-transformers model (saves time on first request)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run with Gunicorn (optimized for free tier)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 300 --graceful-timeout 300 --keep-alive 5 app_render:app