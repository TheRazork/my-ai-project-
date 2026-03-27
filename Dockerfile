FROM python:3.12-slim

# Установка системных зависимостей для pygame
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка pygame через pip (это гарантирует последнюю версию)
RUN pip install pygame

WORKDIR /app
COPY . .

CMD ["python", "flappy.py"]