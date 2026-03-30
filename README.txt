# Flappy Bird

Классическая игра Flappy Bird, реализованная на Python с использованием Pygame. Проект демонстрирует полный цикл разработки: от прототипа до контейнеризации в Docker.

## Особенности игры
- Смена дня и ночи каждые 10 очков
- Система медалей (дерево, бронза, серебро, золото)
- Пауза по клавише `P` или `ESC`
- Движущиеся облака для атмосферы
- Сохранение рекорда текущей сессии

## Управление
| Клавиша | Действие |
|---------|----------|
| **Пробел** / **ЛКМ** | Прыжок / Начать игру |
| **P** / **ESC** | Пауза |
| **R** | Рестарт (в меню паузы) |
| **Q** / **ESC** | Выход (в меню паузы) |

---

## Запуск через Docker

Этот способ не требует установки Python или Pygame на ваш компьютер. Всё необходимое уже внутри контейнера.

### Шаг 1. Установите Docker

- **Windows / macOS**: скачайте и установите [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: установите [Docker Engine](https://docs.docker.com/engine/install/)

После установки запустите Docker Desktop.

---

### Шаг 2. Скачайте код проекта


```bash
git clone https://github.com/TheRazork/my-ai-project-.git
cd my-ai-project-

# Собрать Docker-образ
docker build -t flappy-bird .

# Запустить игру (для Windows, требуется X-сервер, см. Шаг 4)
docker run -it --rm -e DISPLAY=host.docker.internal:0 flappy-bird

# Для отображения окна игры на Windows нужен X-сервер.
Скачать VcXsrv https://sourceforge.net/projects/vcxsrv/

