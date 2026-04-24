WORKDIR /app
COPY ai-engine/main.py .
COPY ai-engine/requirements.txt .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
