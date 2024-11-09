FROM python:3.9-slim

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure wait-for-postgres.sh is executable
RUN chmod +x wait-for-postgres.sh

# Set the entrypoint to run wait-for-postgres.sh and then manager.py
CMD ["./wait-for-postgres.sh", "python", "manager.py"]
