import sqlite3
import time

conn = sqlite3.connect('precos_bot.db')

cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS produtos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               url_kabum TEXT NOT NULL,
               preco_kabum REAL NOT NULL,
               timestamp_ultima_atualizacao REAL NOT NULL
               );
               ''')

nome_produto = "Console PlayStation 5 Slim Sony, SSD 1TB, Edição Digital, Com Controle Sem Fio DualSense, Branco + 2 Jogos Digitais - 1000038914"
url_produto_kabum = "https://www.kabum.com.br/produto/542929/console-playstation-5-slim-sony-ssd-1tb-edicao-digital-com-controle-sem-fio-dualsense-branco-2-jogos-digitais-1000038914"
preco_produto_kabum  = 3553.07
timestamp_atual = time.time()

cursor.execute("INSERT INTO produtos (nome, url_kabum, preco_kabum, timestamp_ultima_atualizacao) VALUES (?, ?, ?, ?)",
               (nome_produto, url_produto_kabum, preco_produto_kabum, timestamp_atual)) #primeiro colocamos ? como placeholder e depois uma tupla com os valores reais

conn.commit() #commit igual github pra mandar as mudancas pro db

print("Dados adicionados com sucesso!")


cursor.execute("SELECT id, nome, preco_kabum, timestamp_ultima_atualizacao FROM produtos") #seleciona dados x de todos os produtos

resultados = cursor.fetchall() #pega esses dados e salva na variavel resultados

print("\n--- Produtos no BD ---")
for produto in resultados: #for loop classico, o objeto produto vem como tupla, com cada coluna numa posicao que eu chamei no SELECT
    print(f"ID: {produto[0]}, Nome: {produto[1]}, Preço Kabum: R${produto[2]:.2f}, Última Att: {time.ctime(produto[3])}") #vai printar todos essas infos de todos os produtos no meu db

#busca personalizada

nome_busca = "Console PlayStation 5 Slim Sony, SSD 1TB, Edição Digital, Com Controle Sem Fio DualSense, Branco + 2 Jogos Digitais - 1000038914"
cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome_busca,))
produto_encontrado = cursor.fetchone() #pega o primeiro
if produto_encontrado:
    print(f"\nProduto encontrado pelo nome: ID: {produto_encontrado[0]}, Nome: {produto_encontrado[1]}")
else:
    print(f"\n Produto '{nome_busca}' não encontrado no banco de dados do bot.")

# Atualizando o preco de um produto

nome_produto_atualizar = "Console PlayStation 5 Slim Sony, SSD 1TB, Edição Digital, Com Controle Sem Fio DualSense, Branco + 2 Jogos Digitais - 1000038914"
novo_preco_kabum = 3499.99
novo_timestamp = time.time()

cursor.execute("UPDATE produtos SET preco_kabum = ?, timestamp_ultima_atualizacao = ? WHERE nome = ?",
               (novo_preco_kabum, novo_timestamp, nome_produto_atualizar))

conn.commit()

print(f"Preço do '{nome_produto_atualizar}' atualizado para R$ {novo_preco_kabum:.2f} e timestamp atualizado.")

cursor.execute("SELECT id, nome, preco_kabum, timestamp_ultima_atualizacao FROM produtos WHERE nome = ?", (nome_produto_atualizar,))
produto_atualizado = cursor.fetchone()

if produto_atualizado:
    print(f"Dados atuais: ID: {produto_atualizado[0]}, Preço Kabum: R${produto_atualizado[2]:.2f}, Última atualizacao: {time.ctime(produto_atualizado[3])}")


#Deletar um produto

preco_produto_deletar = 3499.99

cursor.execute("DELETE FROM produtos WHERE preco_kabum =?", (preco_produto_deletar,))
conn.commit()

print(f"Produtos com preço R${preco_produto_deletar:.2f} deletados com sucesso")

cursor.execute("SELECT id, nome FROM produtos")
print("\n--- Produtos restantes no BD ---")
for produto in cursor.fetchall():
    print(f"ID: {produto[0]}, Nome: {produto[1]}")

conn.close()