# Базовый образ с Python 3.12
FROM python:3.12-slim

# Устанавливаем Pygame и необходимые библиотеки для графики
RUN apt-get update && apt-get install -y \
    python3-pygame \
    libgl1-mesa-glx \
    libegl1 \
    libopengl0 \
    && rm -rf /var/lib/apt/lists/*

# Указываем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . .

# Команда, которая запускается при старте контейнера
CMD ["python", "flappy.py"]