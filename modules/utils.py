import re
from datetime import datetime

def formatar_moeda(valor):
    """Formata valor para moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_data(data_str):
    """Formata data para padrão brasileiro"""
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        return data.strftime('%d/%m/%Y')
    except:
        return data_str

def limpar_texto(texto):
    """Remove caracteres especiais e normaliza texto"""
    texto = re.sub(r'[^\w\s]', ' ', texto)
    return ' '.join(texto.split()).upper()

def calcular_variacao_preco(preco_atual, preco_referencia):
    """Calcula variação percentual do preço"""
    if preco_referencia == 0:
        return 0
    return ((preco_atual - preco_referencia) / preco_referencia) * 100
