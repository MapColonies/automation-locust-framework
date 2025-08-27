# syntax=docker/dockerfile:1.4

############################################
# Build stage: install dependencies
############################################
FROM python:3.12-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

############################################
# Final stage: lean runtime image
############################################
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN addgroup --system appgroup \
 && adduser --system --ingroup appgroup appuser

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

USER appuser

CMD ["python", "create_vector_attribute.py"]
