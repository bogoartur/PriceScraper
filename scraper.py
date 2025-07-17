import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import time


categorias_kabum = ["hardware", "perifericos", "computadores", "gamer", "celular-smartphone", "tv"] ## vou scrapar algumas paginas de todas essas categorias


def get_products_from_category(category_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    }
    response = requests.get(category_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

    if script_tag:
        json_string_outer = script_tag.string
        if json_string_outer:
            outer_json_data = json.loads(json_string_outer)
            inner_json_string = outer_json_data.get('props', {}).get('pageProps', {}).get('data')

            if inner_json_string:
                inner_json_data = json.loads(inner_json_string)

                produtos = inner_json_data.get('catalogServer', {}).get('data')
                listagem = []
                for produto in produtos:
                    
                    nome = produto.get('name')
                    url = "https://www.kabum.com.br/produto/" + str(produto.get('code')) + '/' + produto.get('friendlyName')
                    preco = produto.get('priceWithDiscount')
                    thumbnail_url = produto.get('image')
                    id = produto.get('code')
                    listagem.append((nome, url, preco, thumbnail_url, id))  # Adiciona o produto à lista
                return listagem
                
                    


def update_kabum_database():
    conn = sqlite3.connect('produtos_kabum.db')
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS produtos_kabum (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   url TEXT NOT NULL,
                   preco_atual REAL NOT NULL,
                   menor_preco REAL NOT NULL,
                   timestamp_ultima_atualizacao REAL NOT NULL,
                   timestamp_menor_preco REAL NOT NULL,
                   thumbnail_url TEXT NOT NULL,
                   categoria TEXT NOT NULL,
                   id_kabum INTEGER NOT NULL UNIQUE
                   );
                   ''')
    
    if not cursor.execute("SELECT * FROM produtos_kabum LIMIT 1").fetchone():
        for categoria in categorias_kabum:
            for n in range(1, 4):
                lista_produtos = get_products_from_category(f'https://www.kabum.com.br/{categoria}?page_number={n}&page_size=100&sort=most_searched')
                timestamp_atual = time.time()
                for produto in lista_produtos:
                    cursor.execute("INSERT INTO produtos_kabum (nome, url, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, thumbnail_url, categoria, id_kabum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   (produto[0], produto [1], produto[2], produto[2], timestamp_atual, timestamp_atual, produto[3], categoria, produto[4]))
        conn.commit()
        print("Banco de dados atualizado com sucesso!")
    else:
        for categoria in categorias_kabum:
            for n in range(1, 4):
                
                lista_produtos = get_products_from_category(f'https://www.kabum.com.br/{categoria}?page_number={n}&page_size=100&sort=most_searched')
                timestamp_atual = time.time()
                for produto in lista_produtos:
                    if cursor.execute("SELECT * FROM produtos_kabum WHERE id_kabum = ?", (produto[4],)).fetchone():
                        if produto[2] < cursor.execute("SELECT menor_preco FROM produtos_kabum WHERE id_kabum = ?", (produto[4],)).fetchone()[0]:
                            cursor.execute("UPDATE produtos_kabum SET preco_atual = ?, menor_preco = ?, timestamp_ultima_atualizacao = ?, timestamp_menor_preco = ? WHERE id_kabum = ?",
                                           (produto[2], produto[2], timestamp_atual, timestamp_atual, produto[4]))
                            conn.commit()
                            print(f"Preço do produto {produto[0]} diminuiu, atualizado.")
                        elif produto[2] != cursor.execute("SELECT preco_atual FROM produtos_kabum WHERE id_kabum = ?", (produto[4],)).fetchone()[0]:
                            cursor.execute("UPDATE produtos_kabum SET preco_atual = ?, timestamp_ultima_atualizacao = ? WHERE id_kabum = ?",
                                           (produto[2], timestamp_atual, produto[4]))
                            conn.commit()
                            print(f"Preço do produto {produto[0]} aumentou, atualizado.")
                        else:
                            cursor.execute("UPDATE produtos_kabum SET timestamp_ultima_atualizacao = ? WHERE id_kabum = ?",
                                           (timestamp_atual, produto[4]))
                            conn.commit()
                            print(f"Preço do produto {produto[0]} não mudou, mas o timestamp foi atualizado.")
                    else:
                        cursor.execute("INSERT INTO produtos_kabum (nome, url, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, thumbnail_url, categoria, id_kabum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (produto[0], produto[1], produto[2], produto[2], timestamp_atual, timestamp_atual, produto[3], categoria, produto[4]))
                        conn.commit()
                        print(f"Produto {produto[0]} adicionado ao banco de dados.")
    conn.close()

update_kabum_database()