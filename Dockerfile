FROM python:3.14.3

FROM postgres:17-alpine
EXPOSE 5432

FROM redis:7-alpine
EXPOSE 6379

WORKDIR /app

FROM python:3.14.3

EXPOSE 5432

COPY requirements.txt .
COPY . .
RUN apt-get update && apt-get install -y python3-pip
RUN python -m pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
