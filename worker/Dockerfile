FROM python:3.11-slim

WORKDIR /app

RUN pip install redis psycopg2-binary

COPY worker.py .

CMD ["python", "worker.py"]