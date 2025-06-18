import time
import random
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Histogram

def generate_html(mensagem):
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Minha Aplicação</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            height: 100vh;
            background: linear-gradient(135deg, #990000 0%, #000000 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #ffffff;
            text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
        }}
        h1 {{
            font-size: 3rem;
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1>{mensagem}</h1>
</body>
</html>
"""

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Histograma para análise temporal (latência)
REQUEST_LATENCY = Histogram(
    'app_processing_seconds',
    'Tempo de processamento da requisição',
    ['endpoint']
)

@app.route('/')
def hello():
    with REQUEST_LATENCY.labels(endpoint='/').time():  # ⏱️ Mede tempo com contexto
        delay = random.uniform(2, 5)
        print(f"Adicionando um atraso de {delay:.2f} segundos...")
        time.sleep(delay)

        mensagem = f"Olá! Esta é a v-quebrada.<br>Processamento demorou {delay:.2f} segundos."
        return generate_html(mensagem)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
