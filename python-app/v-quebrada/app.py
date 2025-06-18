import time
import random
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

# --- Função para gerar HTML ---
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

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)

# --- Configuração das Métricas do Prometheus ---
# Adiciona métricas padrão (ex: latência e contagem de requisições)
metrics = PrometheusMetrics(app)

# Registra uma métrica customizada do tipo Gauge para medir o tempo de processamento da tarefa "lenta".
# Um Gauge é um valor que pode arbitrariamente subir e descer.
processing_time_gauge = metrics.info('app_processing_seconds', 'Tempo gasto no processamento da tarefa lenta')

# --- Rotas da Aplicação ---

@app.route('/')
def hello():
    """
    Endpoint principal que simula uma alta latência de forma intermitente.
    """
    start_time = time.time()
    
    # Simula um processamento lento. Vamos fazer com que a latência seja alta na maioria das vezes.
    # Gera um número aleatório entre 2 e 5.
    delay = random.uniform(2, 5) 
    print(f"Adicionando um atraso de {delay:.2f} segundos...")
    time.sleep(delay) # Adiciona o atraso
    
    processing_time = time.time() - start_time
    
    # Atualiza o valor da nossa métrica customizada com o tempo de processamento.
    processing_time_gauge.set(processing_time)
    
    # Cria a mensagem que será exibida no H1
    mensagem = f"Olá! Esta é a v-quebrada.<br>Processamento demorou {processing_time:.2f} segundos."
    
    # Retorna o HTML com a mensagem inserida no H1
    return generate_html(mensagem)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
