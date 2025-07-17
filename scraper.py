import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import time

def get_product_price_from_kabum(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    }
    response = requests.get(product_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})

    if script_tag:
        json_data = json.loads(script_tag.string)
        props = json_data.get('props', None)
        page_props = props.get('pageProps', None)
        product = page_props.get('product', None)
        prices = product.get('prices', None)
        price_with_discount = prices.get('priceWithDiscount', None) #chegando na tag de preco da kabum, algoritmo especifico pra kabum

        print(f"7. 'priceWithDiscount' encontrado: {price_with_discount}")
        return float(price_with_discount)




categorias_kabum = ["hardware", "perifericos", "computadores", "gamer", "celular-smartphone", "tv"] ## vou scrapar algumas paginas de todas essas categorias

# --- Exemplo de uso ---
product_url = "https://www.kabum.com.br/produto/527400/console-playstation-5-slim-sony-ssd-1tb-com-controle-sem-fio-dualsense-branco-2-jogos-1000038899"

price = get_product_price_from_kabum(product_url)

print(f"\nRESULTADO FINAL: O preço com desconto do produto é: R$ {price:.2f}")


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
                
                for produto in produtos:
                    
                    nome = produto.get('name')
                    url = "https://www.kabum.com.br/produto/" + str(produto.get('code')) + '/' + produto.get('friendlyName')
                    preco = produto.get('priceWithDiscount')
                    thumbnail_url = produto.get('image')
                    id = produto.get('code')
                    return nome, url, preco, thumbnail_url, id
                    


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
                produto = get_products_from_category(f'https://www.kabum.com.br/{categoria}?page_number={n}&page_size=100&sort=most_searched')
                timestamp_atual = time.time()

                cursor.execute("INSERT INTO produtos_kabum (nome, url, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, thumbnail_url, categoria, id_kabum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (produto[0], produto [1], produto[2], produto[2], timestamp_atual, timestamp_atual, produto[3], categoria, produto[4]))
        conn.commit()
        print("Banco de dados atualizado com sucesso!")
    else:
        for categoria in categorias_kabum:
            for n in range(1, 4):
                produto = get_products_from_category(f'https://www.kabum.com.br/{categoria}?page_number={n}&page_size=100&sort=most_searched')
                timestamp_atual = time.time()

                if cursor.execute("SELECT * FROM produtos_kabum WHERE id_kabum = ?", (produto[4],)).fetchone():
                    if produto[2] < cursor.execute("SELECT menor_preco FROM produtos_kabum WHERE id_kabum = ?", (produto[4],)).fetchone()[0]:
                        cursor.execute("UPDATE produtos_kabum SET preco_atual = ?, menor_preco = ?, timestamp_ultima_atualizacao = ?, timestamp_menor_preco = ? WHERE id_kabum = ?",
                                       (produto[2], produto[2], timestamp_atual, timestamp_atual, produto[4]))
                    elif produto[2] != cursor.execute("SELECT preco_atual FROM produtos_kabum WHERE id_kabum = ?", (produto[4],)).fetchone()[0]:
                        cursor.execute("UPDATE produtos_kabum SET preco_atual = ?, timestamp_ultima_atualizacao = ? WHERE id_kabum = ?",
                                       (produto[2], timestamp_atual, produto[4]))
                    else:
                        cursor.execute("UPDATE produtos_kabum SET timestamp_ultima_atualizacao = ? WHERE id_kabum = ?",
                                       (timestamp_atual, produto[4]))
                else:
                    cursor.execute("INSERT INTO produtos_kabum (nome, url, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, thumbnail_url, categoria, id_kabum) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   (produto[0], produto[1], produto[2], produto[2], timestamp_atual, timestamp_atual, produto[3], categoria, produto[4]))
                