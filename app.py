from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime
from modules.analisador import AnalisadorLicitacoes
from modules.database import Database

app = Flask(_name_)
db = Database()

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
    """Retorna todas as licitações de Vinhedo"""
    try:
        with open('data/vinhedo_licitacoes.json', 'r', encoding='utf-8') as f:
            licitacoes = json.load(f)
        return jsonify(licitacoes)
    except:
        return jsonify([])

@app.route('/api/analise')
def api_analise():
    """Analisa irregularidades"""
    analisador = AnalisadorLicitacoes()
    resultado = analisador.analisar_todas()
    return jsonify(resultado)

@app.route('/api/comparar', methods=['POST'])
def api_comparar():
    """Compara preços entre prefeituras"""
    dados = request.get_json()
    produto = dados.get('produto', '')
    
    analisador = AnalisadorLicitacoes()
    comparacao = analisador.comparar_preco(produto)
    return jsonify(comparacao)

if _name_ == '_main_':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
