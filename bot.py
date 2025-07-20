import logging
import sqlite3
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Application, CallbackQueryHandler, CommandHandler, ContextTypes, InlineQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Olá, esse bot de preços é um projeto de férias em desenvolvimento por Artur Bogo. O único objetivo é de estudo e aprendizado. Você pode me encontrar no GitHub: bogoartur, ou no LinkedIn: Artur Bogo." \
    "\nSelecione uma opção abaixo para navegar pelas categorias de produtos disponíveis para consulta de preços.")
    keyboard = [
        [
            InlineKeyboardButton("Hardware", callback_data='hardware'),
            InlineKeyboardButton("Periféricos", callback_data='perifericos'),
        ]
    ]
    keyboard.append([
        InlineKeyboardButton("Computadores", callback_data='computadores'),
        InlineKeyboardButton("Gamer", callback_data='gamer'),
    ])
    keyboard.append([
        InlineKeyboardButton("Smartphones", callback_data='celular-smartphone'),
        InlineKeyboardButton("TVs", callback_data='tv'),
    ])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Escolha uma categoria para ver os produtos disponíveis:",
        reply_markup=reply_markup
    )

async def pesquisa_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Você pesquisou por: {query}. Esses são os resultados:")
    conn, cursor = connect_db()
    cursor.execute("SELECT nome, thumbnail_url, id_kabum, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, url FROM produtos_kabum WHERE nome LIKE ? LIMIT 10", ('%' + query + '%',))
    produtos = cursor.fetchall()
    results = []
    for produto in produtos:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=produto[1],
            caption=f"{produto[0]} \nPreço atual: R$ {produto[3]:.2f} \nMenor preço registrado: R$ {produto[4]:.2f} em {time.ctime(produto[6])}. \n{produto[7]}"
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"{query.data}")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if not query:
        return
    results = []
    conn, cursor = connect_db()
    cursor.execute("SELECT nome, thumbnail_url, id_kabum, preco_atual, menor_preco, timestamp_ultima_atualizacao, timestamp_menor_preco, url FROM produtos_kabum WHERE nome LIKE ? LIMIT 10", ('%' + query + '%',))
    produtos = cursor.fetchall()
    for produto in produtos:
        cursor.execute("")
        results.append(
            InlineQueryResultArticle(
                id=produto[2],
                title=produto[0],
                thumbnail_url=produto[1],
                description=f"R$ {produto[3]:.2f}",
                input_message_content=
                InputTextMessageContent(
                    f"{produto[0]}"
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
    pesquisa_handler = MessageHandler(filters.TEXT, pesquisa_produto)
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(pesquisa_handler)
    application.run_polling()