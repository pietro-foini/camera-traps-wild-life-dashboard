FROM python:3.11-slim AS builder

WORKDIR /app

# Install system build dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  build-essential \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry.
RUN pip install --no-cache-dir poetry==2.4.1

# Copy dependency files.
COPY pyproject.toml poetry.lock* ./

# Configure poetry to create the virtual environment in the project root (.venv).
RUN poetry config virtualenvs.in-project true \
  && poetry install --only main --no-root

FROM python:3.11-slim AS runner

WORKDIR /app

# Copy built virtual environment from the builder stage.
COPY --from=builder /app/.venv /app/.venv

# Copy application source code.
COPY camera_traps/ ./camera_traps/

# Add the virtual environment to PATH.
ENV PATH="/app/.venv/bin:$PATH"

# Expose application port.
EXPOSE 8050

# Run Gunicorn directly as the primary process.
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "1", "--worker-class", "gthread", "--threads", "2", "--timeout", "120", "camera_traps.api.app:app"]