FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["gunicorn", "server:app", "-b", "0.0.0.0:80", "--log-file", "-", "--access-logfile", "-"]