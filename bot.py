import logging
import sqlite3
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Application, CallbackQueryHandler, CommandHandler, ContextTypes, InlineQueryHandler
import scraper
from scraper import get_product_price_from_kabum

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Olá, esse bot de preços é um projeto de férias em desenvolvimento por Artur Bogo. O único objetivo é de estudo e aprendizado. Você pode me encontrar no GitHub: bogoartur, ou no LinkedIn: Artur Bogo." \
    "\nDigite @ArturKabum_bot seguido do nome de um produto para realizar uma pesquisa, ou envie o nome do produto no chat sem @ para ver o top 10 encontrados.")
    # keyboard = [
    #     [
    #         InlineKeyboardButton("Hardware", callback_data='hardware'),
    #         InlineKeyboardButton("Periféricos", callback_data='perifericos'),
    #     ]
    # ]
    # keyboard.append([
    #     InlineKeyboardButton("Computadores", callback_data='computadores'),
    #     InlineKeyboardButton("Gamer", callback_data='gamer'),
    # ])
    # keyboard.append([
    #     InlineKeyboardButton("Smartphones", callback_data='celular-smartphone'),
    #     InlineKeyboardButton("TVs", callback_data='tv'),
    # ])
    # reply_markup = InlineKeyboardMarkup(keyboard)

    # await update.message.reply_text(
    #     "Escolha uma categoria para ver os produtos disponíveis:",
    #     reply_markup=reply_markup
    # )

def connect_db_usuario():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   id_telegram INTEGER NOT NULL UNIQUE,
                   favoritados TEXT NOT NULL DEFAULT ''
                   );
                   ''')
    conn.commit()
    return conn, cursor

async def favoritar_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    produto = query.data.split("_")[1]
    conn, cursor = connect_db_usuario()
    cursor.execute("SELECT * FROM usuarios WHERE id_telegram = ?", (update.effective_user.id,))
    usuario = cursor.fetchone()
    if not usuario:
        cursor.execute("INSERT INTO usuarios (id_telegram, favoritados) VALUES (?, ?)", (update.effective_user.id, ''))
        conn.commit()
        usuario = (update.effective_user.id, '',)
    
    if len(usuario[2]) > 1:
        favoritados = usuario[2].split(",") 
    elif len(usuario[2]) == 1:
        favoritados = [usuario[2]]
    else:
        favoritados = []

    resposta = ""
    if produto not in favoritados:
        resposta = "Produto adicionado aos favoritos!"
        btn_text = "Remover favorito"
        favoritados.append(produto)
        cursor.execute("UPDATE usuarios SET favoritados = ? WHERE id_telegram = ?", (','.join(favoritados), update.effective_user.id))
        conn.commit()
        await query.edit_message_text(text=f"Produto adicionado aos favoritos!")
    else:
        resposta = "Produto removido dos favoritos!"
        btn_text = "Favoritar produto"
        favoritados.remove(produto)
        cursor.execute("UPDATE usuarios SET favoritados = ? WHERE id_telegram = ?", (','.join(favoritados), update.effective_user.id))
        conn.commit()
        await query.edit_message_text(text=f"Produto removido dos favoritos!")
    

async def favoritos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn, cursor = connect_db_usuario()
    conn_produtos, cursor_produtos = scraper.connect_db()
    cursor.execute("SELECT * FROM usuarios WHERE id_telegram = ?", (update.effective_user.id,))
    usuario = cursor.fetchone()
    if not usuario or not usuario[1]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Você não tem produtos favoritos.")
        return
    else:
        if len(usuario[2]) > 1:
            favoritos = usuario[2].split(',')
        produtos_favoritos = []
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Esses são seus favoritos, amigo:")
        for produto_id in favoritos:
            
            cursor_produtos.execute("SELECT nome, thumbnail_url, id_kabum, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, url FROM produtos_kabum WHERE id_kabum = ?", (produto_id,))
            atualizado_produto = cursor_produtos.fetchone()
            if atualizado_produto[5] < time.time() - 43200:
                get_product_price_from_kabum(produto[7])  # Atualiza o preço d o produto
                cursor.execute("SELECT nome, thumbnail_url, id_kabum, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, url FROM produtos_kabum WHERE id_kabum = ? LIMIT 1", (produto[2],))
                atualizado_produto = cursor.fetchone()
            await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=atualizado_produto[1],
            caption=f"{atualizado_produto[0]} \n\nPreço atual: R$ {atualizado_produto[3]:.2f} \n\nMenor preço registrado: R$ {atualizado_produto[4]:.2f} em {time.ctime(atualizado_produto[6])}. \n\n{atualizado_produto[7]}"
            )
            ja_favoritado = produto_id in favoritos
            if ja_favoritado:
                keyboard = [
                    [
                        InlineKeyboardButton("Remover favorito", callback_data=f"favoritar_{atualizado_produto[2]}"),
                    ]
                ]
            else:
                keyboard = [
                    [
                        InlineKeyboardButton("Favoritar produto", callback_data=f"favoritar_{atualizado_produto[2]}"),
                    ]
                ]   
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Remover favorito?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

async def pesquisa_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    conn, cursor = connect_db()
    cursor.execute("SELECT nome, thumbnail_url, id_kabum, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, url FROM produtos_kabum WHERE nome LIKE ? LIMIT 5", ('%' + query + '%',))
    produtos = cursor.fetchall()
    if not produtos:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Desculpa colega, não tenho esse produto na minha base de dados para rastreio ainda.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Encontrei estes produtos com sua busca, amigo:")
    for produto in produtos:
        if produto[5] < time.time() - 43200:
            get_product_price_from_kabum(produto[7])  # Atualiza o preço d o produto
        cursor.execute("SELECT nome, thumbnail_url, id_kabum, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, url FROM produtos_kabum WHERE id_kabum = ? LIMIT 1", (produto[2],))
        atualizado_produto = cursor.fetchone()
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=atualizado_produto[1],
            caption=f"{atualizado_produto[0]} \n\nPreço atual: R$ {atualizado_produto[3]:.2f} \n\nMenor preço registrado: R$ {atualizado_produto[4]:.2f} em {time.ctime(atualizado_produto[6])}. \n\n{atualizado_produto[7]}"
        )
        keyboard = [
            [
                InlineKeyboardButton("Favoritar produto", callback_data=f"favoritar_{atualizado_produto[2]}"),
            ]
        ]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Favoritar produto?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if not query:
        return
    results = []
    conn, cursor = connect_db()
    cursor.execute("SELECT nome, thumbnail_url, id_kabum, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, url FROM produtos_kabum WHERE nome LIKE ? LIMIT 10", ('%' + query + '%',))
    produtos = cursor.fetchall()
    for produto in produtos:
        if produto[5] < time.time() - 43200:
            get_product_price_from_kabum(produto[7])  # Atualiza o preço do produto
        cursor.execute("SELECT nome, thumbnail_url, id_kabum, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, url FROM produtos_kabum WHERE id_kabum = ? LIMIT 1", (produto[2],))
        atualizado_produto = cursor.fetchone()
        results.append(
            InlineQueryResultArticle(
                id=str(atualizado_produto[2]),
                title=atualizado_produto[0],
                thumbnail_url=atualizado_produto[1],
                description=f"R$ {atualizado_produto[3]:.2f}",
                input_message_content=
                InputTextMessageContent(
                    f"{atualizado_produto[0]}"
                )
            )
        )
    await update.inline_query.answer(results)

def connect_db():
    conn = sqlite3.connect("produtos_kabum.db")
    cursor = conn.cursor()
    return conn, cursor

if __name__ == '__main__':
    with open('token_telegram.txt', 'r') as file:
        token = file.read().strip()
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(CommandHandler('favoritos', favoritos))
    pesquisa_handler = MessageHandler(filters.TEXT, pesquisa_produto)
    application.add_handler(start_handler)

    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(pesquisa_handler)

    application.add_handler(CallbackQueryHandler(favoritar_produto, pattern=r'^favoritar_'))
    application.run_polling()