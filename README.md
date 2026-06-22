# Лаб. работа №6 Docker compose

## 1. Cоздаем приложение на python:  
- в `requirements.txt` указываем зависимости:
```txt
flask
redis
```
- в `app.py` пишем код python:  
```python
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    return cache.incr('hits')

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```
При этом, используем файл с переменными окружения `.env` - модуль load_dotenv автоматически считывает значения из этого файла  

## 2. пишем dockerfile для сборки образа веб-приложения:  
- для сборки используем стартовый образ `python:3.12-slim`, определяем рабочую директорию приложения `/app`
- определяем переменные среды `FLASK_APP=app.py`, `FLASK_RUN_HOST=0.0.0.0`  
- копируем зависимости `requirements.txt` и устанавливаем через `pip install -r requirements.txt`  
- определяем внутренний порт контейнера, на который будем пробрасывать внешний порт для обращения к приложению `EXPOSE 5000`  
- копируем код python-приложения и запускаем через команду `CMD ["flask", "run", "--debug"]`
```dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

COPY app.py .

CMD ["flask", "run", "--debug"]
```

## 3. Описываем файл `docker-compose.yml` для сборки flask+redis стека:  
```yml
services:
  web:
    build: .
    ports:
      - "8000:5000"
  
  redis:
    image: "redis:alpine"
```
Проверяем сборку docker compose командой `docker compose up -d`, при обращении к http://localhost:8000 должны получить вывод:  
```bash
$ curl http://localhost:8000
Hello World! I have been seen 6 times.  
$ curl http://localhost:8000
Hello World! I have been seen 7 times.
```

