FROM python:3.10-slim

LABEL maintainer="FinAgent Team"
LABEL description="FinAgent Unified - 金融智能顾问统一平台"

# ==================
# System dependencies
# ==================
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ==================
# Working directory
# ==================
WORKDIR /app

# ==================
# Python dependencies
# ==================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==================
# Application code
# ==================
COPY . .

# ==================
# Environment variables
# ==================
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ==================
# Expose ports
# ==================
EXPOSE 5000 8000 7860

# ==================
# Health check
# ==================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/v1/health || exit 1

# ==================
# Default command
# ==================
CMD ["python", "-m", "src.api.main"]
