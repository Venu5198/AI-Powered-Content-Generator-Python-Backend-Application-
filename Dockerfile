# --- Builder Stage ---
FROM python:3.11-alpine as builder

WORKDIR /app

# Install build dependencies and build wheels
# Wheels are pre-compiled and easier to just copy over without the build tools
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev g++ && \
    pip install --upgrade pip

COPY requirements.txt .

# Build wheels directly to avoid caching intermediate files
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# --- Final Stage ---
FROM python:3.11-alpine

WORKDIR /app

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production

# Install only minimum runtime libraries
RUN apk add --no-cache libstdc++

# Copy wheels from builder and install them, then immediately delete them to save space
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY . .

# Setup directories and non-root user in one step to reduce layers
RUN mkdir -p /app/data && \
    adduser -D appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"]
