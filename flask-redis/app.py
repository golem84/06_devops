import redis
from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# Создаем метрику-счетчик для посещений
REQUEST_COUNT = Counter(
    'flask_site_visits_total', 
    'Total number of site visits'
)

def get_hit_count():
    return cache.incr('hits')

@app.route('/')
def hello():
    # Увеличиваем счетчик Prometheus при каждом посещении
    REQUEST_COUNT.inc()
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

# Нативный endpoint для Prometheus
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)