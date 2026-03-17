# ================================================
#  docker/Dockerfile
#  Python 3.12 + Flask + MySQL client
# ================================================

FROM python:3.12-slim

# Dépendances système pour PyMySQL / mysqlclient
RUN apt-get update && apt-get install -y \
      default-libmysqlclient-dev \
      gcc \
      pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["python", "app.py"]
