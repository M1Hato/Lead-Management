# Використовуємо легкий образ Python
FROM python:3.13-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо список залежностей
COPY requirements.txt .

# Встановлюємо бібліотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код сервісу
COPY . .

# Команда для запуску (її ми перепишемо в docker-compose для кожного сервісу)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]