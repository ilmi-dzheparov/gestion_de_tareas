FROM python:3.11-slim

# Настройки Python, чтобы логи выводились сразу
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Дополнительно устанавливаем gunicorn, если его нет в requirements.txt
RUN pip install gunicorn

COPY . .

# Информируем (необязательно, Render сам найдет порт)
EXPOSE 8000

# ГЛАВНОЕ ИЗМЕНЕНИЕ: используем gunicorn и переменную $PORT
# Замени 'myproject.wsgi' на путь к твоему wsgi-файлу (обычно название_папки_с_settings.wsgi)
CMD gunicorn --bind 0.0.0.0:$PORT myproject.wsgi:application