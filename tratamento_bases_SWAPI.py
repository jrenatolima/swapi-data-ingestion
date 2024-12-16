import pandas as pd
import os
import re

# Criar pasta 'work' se não existir
os.makedirs('work', exist_ok=True)

# Função para tratar os dados
def tratar_dados(arquivo_csv, categoria):
    # Carregar os dados
    df = pd.read_csv(f"raw/{arquivo_csv}")
    
    # Padronizar strings para lower case
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    
    # Remover caracteres especiais
    df = df.applymap(lambda x: re.sub(r'[^a-z0-9\s.,:/-]', '', x) if isinstance(x, str) else x)
    
    # Salvar os dados tratados na pasta 'work'
    df.to_csv(f"work/{categoria}.csv", index=False)
    print(f"Dados de {categoria} tratados e salvos em work/{categoria}.csv")

# Tratamento das bases de dados
tratar_dados("people.csv", "people")
tratar_dados("planets.csv", "planets")
tratar_dados("films.csv", "films")
