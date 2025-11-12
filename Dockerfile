# Imagen base ligera de Python
FROM python:3.11-slim

# Evitar *.pyc y forzar logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app

# Instala dependencias primero (mejor cacheo)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "functions-framework==3.*"

# Copia el resto del código
COPY . .

# (Opcional pero útil si tus paquetes no tienen __init__.py)
# ENV PYTHONPATH=/app

# Variables para Cloud Functions/Run
# - FUNCTION_TARGET: nombre de tu función (entry_point)
# - FUNCTION_SIGNATURE_TYPE: http porque tu función recibe 'request'
ENV FUNCTION_TARGET=entry_point \
    FUNCTION_SIGNATURE_TYPE=http

# Cloud Run/Functions exponen el servicio en $PORT (por defecto 8080)
EXPOSE 8080

# Arranca Functions Framework
CMD ["functions-framework", "--target=entry_point", "--port=8080"]
