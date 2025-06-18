from flask import Flask, render_template_string
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Minha Aplicação</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            background: linear-gradient(5deg, #a8edea 0%, #65c18c 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #ffffff;
            text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
        }
        h1 {
            font-size: 3rem;
        }
    </style>
</head>
<body>
    <h1>Olá! Esta é a v2 da minha aplicação.</h1>
</body>
</html>
"""

@app.route('/')
def hello():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
