FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
# Si usas hilos, mejor evita setlocale del sistema (ver nota al final)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
