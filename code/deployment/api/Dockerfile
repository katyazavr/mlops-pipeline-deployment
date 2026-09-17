# Build context is the repository root (see docker-compose.yml), so paths
# below are relative to the repo root, not this file's folder.
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY code/deployment/api/main.py .
COPY models/model.joblib models/model.joblib

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
