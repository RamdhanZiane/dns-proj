FROM python:3.9-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x wait-for-postgres.sh

RUN ./wait-for-postgres.sh
CMD ["python", "manager.py"]
