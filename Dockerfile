FROM python:3.11-slim

WORKDIR /app

# Copy from the ai-engine folder
COPY ai-engine/main.py .
COPY ai-engine/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
