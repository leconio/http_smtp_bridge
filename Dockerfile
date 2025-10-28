# Multi-stage build for production SMTP Bridge
FROM python:3.11-alpine AS builder

# Install build dependencies and uv
RUN apk add --no-cache gcc musl-dev libffi-dev && \
    pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.11-alpine

# Install runtime dependencies
RUN apk add --no-cache curl

# Create non-root user
RUN adduser -D -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY app ./app
COPY gunicorn_conf.py ./

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run with gunicorn
CMD ["gunicorn", "-c", "gunicorn_conf.py", "app.main:app"]
