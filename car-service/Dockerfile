FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi[all] ariadne sqlite-utils

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
