# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем пакетный менеджер и устанавливаем system-зависимости
RUN apt update && apt install -y libpq-dev gcc

# Обновляем pip и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копируем код проекта в контейнер
COPY . .

# Открываем порт
EXPOSE 8000

# Запуск сервера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "my_project.wsgi:application"]

