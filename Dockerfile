FROM python:3.13.7-slim-trixie
WORKDIR /app

# (Optional) If you use non-binary psycopg or cryptography, you may need build deps:
# RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose is informational; Railway still injects $PORT
EXPOSE 8000

# Entrypoint: run migrations, then start server bound to $PORT
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/bin/sh","/entrypoint.sh"]
