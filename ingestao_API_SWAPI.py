import requests
import pandas as pd
import os
from time import sleep

#Criar pasta raw 
os.makedirs('raw', exist_ok=True)

#Função para processar listas e remover quebras de linha (pois estava trazendo um csv com falhas por conta do normalize no fim do código)
def processar_dados(dados, chaves_lista):
    for item in dados:
        #Processar listas
        for chave in chaves_lista:
            if chave in item and isinstance(item[chave], list):
                item[f"{chave}_count"] = len(item[chave])
                item[chave] = ", ".join(item[chave][:3]) + "..." if len(item[chave]) > 3 else ", ".join(item[chave])

        #Remover quebras de linha em todos os campos de texto
        for chave, valor in item.items():
            if isinstance(valor, str):
                item[chave] = valor.replace("\n", " ").replace("\r", " ")
    return dados

#Função para coletar dados da API SWAPI
def coletar_dados(api_url, categoria, paginas=5):
    dados = []
    chaves_lista = ["characters", "planets", "species", "vehicles", "starships"]

    if categoria == "films":  #Caso films (sem paginação)
        url = api_url
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                results = response.json().get('results', [])
                dados.extend(processar_dados(results, chaves_lista))
            else:
                print(f"Erro: Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")
    else:  #Casos paginados (people e planets)
        for page in range(1, paginas + 1):
            url = f"{api_url}?page={page}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    results = response.json().get('results', [])
                    dados.extend(processar_dados(results, chaves_lista))
                    sleep(1)
                else:
                    print(f"Erro: Status {response.status_code}")
            except requests.exceptions.RequestException:
                break

    #Salvar em CSV na pasta Raw
    if dados:
        df = pd.json_normalize(dados)
        df.to_csv(f"raw/{categoria}.csv", index=False)
        print("Dados carregados!")

# Coleta dos dados (utilizando a função criada)
coletar_dados("https://swapi.py4e.com/api/people/", "people")
coletar_dados("https://swapi.py4e.com/api/planets/", "planets")
coletar_dados("https://swapi.py4e.com/api/films/", "films")
