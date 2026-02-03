import json
import pandas as pd
from datetime import datetime

class AnalisadorLicitacoes:
    def _init_(self):
        self.precos_referencia = self.carregar_precos_referencia()
        self.licitacoes = self.carregar_licitacoes()
    
    def carregar_precos_referencia(self):
        try:
            with open('data/referencia_precos.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def carregar_licitacoes(self):
        try:
            with open('data/vinhedo_licitacoes.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def analisar_todas(self):
        alertas = []
        
        for lic in self.licitacoes:
            # Verifica preços acima da média
            if 'itens' in lic:
                for item in lic['itens']:
                    descricao = item.get('descricao', '').lower()
                    valor_unit = item.get('valor_unitario', 0)
                    
                    # Compara com preços de referência
                    for ref_produto, ref_preco in self.precos_referencia.items():
                        if ref_produto.lower() in descricao:
                            if valor_unit > ref_preco * 1.5:  # 50% acima
                                alertas.append({
                                    'tipo': 'SUPERFATURAMENTO',
                                    'licitacao': lic.get('numero', 'N/A'),
                                    'item': descricao,
                                    'valor_vinhedo': valor_unit,
                                    'valor_referencia': ref_preco,
                                    'diferenca_percentual': round(((valor_unit - ref_preco) / ref_preco) * 100, 2)
                                })
            
            # Verifica licitações com valor muito baixo (dispensa indevida)
            if lic.get('valor', 0) > 80000 and lic.get('modalidade') == 'Dispensa':
                alertas.append({
                    'tipo': 'MODALIDADE_INADEQUADA',
                    'licitacao': lic.get('numero', 'N/A'),
                    'valor': lic.get('valor'),
                    'modalidade': lic.get('modalidade'),
                    'mensagem': 'Valor acima de R$ 80.000 em dispensa de licitação'
                })
        
        return {
            'total_licitacoes': len(self.licitacoes),
            'total_alertas': len(alertas),
            'alertas': alertas
        }
    
    def comparar_preco(self, produto_busca):
        resultados = []
        
        for lic in self.licitacoes:
            if 'itens' in lic:
                for item in lic['itens']:
                    if produto_busca.lower() in item.get('descricao', '').lower():
                        resultados.append({
                            'municipio': 'Vinhedo',
                            'licitacao': lic.get('numero'),
                            'data': lic.get('data_publicacao'),
                            'produto': item.get('descricao'),
                            'valor_unitario': item.get('valor_unitario'),
                            'quantidade': item.get('quantidade')
                        })
        
        # Adiciona preços de referência de outras prefeituras
        for municipio, produtos in self.precos_referencia.get('outros_municipios', {}).items():
            for prod, preco in produtos.items():
                if produto_busca.lower() in prod.lower():
                    resultados.append({
                        'municipio': municipio,
                        'licitacao': 'Referência',
                        'data': '-',
                        'produto': prod,
                        'valor_unitario': preco,
                        'quantidade': 1
                    })
        
        return resultados
