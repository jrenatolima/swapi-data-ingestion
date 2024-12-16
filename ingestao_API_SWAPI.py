import requests
import pandas as pd
import os
from time import sleep

# Criar pasta raw se não existir
os.makedirs('raw', exist_ok=True)

# Função para processar listas e remover quebras de linha
def processar_dados(dados, chaves_lista):
    for item in dados:
        # Processar listas (para encurtar e contar os elementos)
        for chave in chaves_lista:
            if chave in item and isinstance(item[chave], list):
                item[f"{chave}_count"] = len(item[chave])
                item[chave] = ", ".join(item[chave][:3]) + "..." if len(item[chave]) > 3 else ", ".join(item[chave])

        # Remover quebras de linha em todos os campos de texto
        for chave, valor in item.items():
            if isinstance(valor, str):
                item[chave] = valor.replace("\n", " ").replace("\r", " ")
    return dados

# Função para coletar dados da API SWAPI
def coletar_dados(api_url, categoria, paginas=5):
    dados = []
    chaves_lista = ["characters", "planets", "species", "vehicles", "starships"]

    if categoria == "films":  # Caso 'films' (sem paginação)
        url = api_url
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                results = response.json().get('results', [])
                dados.extend(processar_dados(results, chaves_lista))
                print("Dados de films coletados e processados com sucesso.")
            else:
                print(f"Erro ao coletar films: Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição de films: {e}")
    else:  # Caso paginado
        for page in range(1, paginas + 1):
            url = f"{api_url}?page={page}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    results = response.json().get('results', [])
                    dados.extend(processar_dados(results, chaves_lista))
                    print(f"Página {page} coletada e processada com sucesso.")
                    sleep(1)
                else:
                    print(f"Erro na página {page}: Status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Erro na página {page}: {e}")
                break

    # Salvar em CSV
    if dados:
        df = pd.json_normalize(dados)
        df.to_csv(f"raw/{categoria}.csv", index=False)
        print(f"Dados de {categoria} salvos em raw/{categoria}.csv")
    else:
        print(f"Não foi possível coletar dados de {categoria}.")

# Coleta dos dados
coletar_dados("https://swapi.py4e.com/api/people/", "people")
coletar_dados("https://swapi.py4e.com/api/planets/", "planets")
coletar_dados("https://swapi.py4e.com/api/films/", "films")