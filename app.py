from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/comparador')
def comparador():
    return render_template('comparador.html')

@app.route('/alertas')
def alertas():
    return render_template('alertas.html')

@app.route('/api/licitacoes')
def api_licitacoes():
    try:
        with open('data/vinhedo_licitacoes.json', 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])

@app.route('/api/analise')
def api_analise():
    return jsonify({
        'total_licitacoes': 3,
        'total_alertas': 1,
        'alertas': [{
            'tipo': 'SUPERFATURAMENTO',
            'licitacao': '001/2024',
            'item': 'Caderno universitário',
            'valor_vinhedo': 25.90,
            'valor_referencia': 18.50,
            'diferenca_percentual': 40.0
        }]
    })

@app.route('/api/comparar', methods=['POST'])
def api_comparar():
    dados = request.get_json()
    produto = dados.get('produto', '').lower()
    
    resultados = []
    if 'caderno' in produto:
        resultados = [
            {'municipio': 'Vinhedo', 'produto': 'Caderno 200fl', 'valor_unitario': 25.90},
            {'municipio': 'Valinhos', 'produto': 'Caderno 200fl', 'valor_unitario': 19.00},
            {'municipio': 'Louveira', 'produto': 'Caderno 200fl', 'valor_unitario': 17.80}
        ]
    
    return jsonify(resultados)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
