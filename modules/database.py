import sqlite3
import json
from datetime import datetime

class Database:
    def _init_(self, db_path='data/licitacoes.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS licitacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT,
                orgao TEXT,
                objeto TEXT,
                valor REAL,
                data_publicacao TEXT,
                situacao TEXT,
                municipio TEXT DEFAULT 'Vinhedo'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                licitacao_id INTEGER,
                descricao TEXT,
                quantidade INTEGER,
                valor_unitario REAL,
                valor_total REAL,
                FOREIGN KEY (licitacao_id) REFERENCES licitacoes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def inserir_licitacao(self, dados):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO licitacoes (numero, orgao, objeto, valor, data_publicacao, situacao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (dados['numero'], dados['orgao'], dados['objeto'], 
              dados['valor'], dados['data_publicacao'], dados['situacao']))
        
        conn.commit()
        conn.close()
