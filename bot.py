import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Application, CallbackQueryHandler, CommandHandler, ContextTypes

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

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"{query.data}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
    with open('token_telegram.txt', 'r') as file:
        token = file.read().strip()
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()