from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app) # Adiciona métricas padrão como latência e contagem de requisições

@app.route('/')
def hello():
    return "Olá! Esta é a v1 da minha aplicação."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)