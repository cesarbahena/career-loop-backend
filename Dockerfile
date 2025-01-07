# Stage 1: Build stage to install dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY ./app /app/app

# Expose port and run the application
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
