FROM python:3.9-slim

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x wait-for-postgres.sh

CMD ["./wait-for-postgres.sh", "python", "manager.py"]
