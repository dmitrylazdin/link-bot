import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
URL_WRITER = os.getenv("CHANNEL_URL_WRITER")
URL_EDITOR = os.getenv("CHANNEL_URL_EDITOR")

GREETING = (
    "Добрый день! Спасибо, что откликнулись.\n"
    "Вас интересует вакансия сценариста или монтажера?"
)

def main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("📖 Вакансия сценариста", url=URL_WRITER)],
        [InlineKeyboardButton("🎬 Вакансия монтажера", url=URL_EDITOR)],
    ]
    return InlineKeyboardMarkup(buttons)

async def send_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(
        GREETING,
        reply_markup=main_keyboard(),
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_menu(update, context)

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # На любое сообщение показываем меню ещё раз
    await send_menu(update, context)

def main():
    if not BOT_TOKEN or not URL_WRITER or not URL_EDITOR:
        raise RuntimeError("Укажите BOT_TOKEN, CHANNEL_URL_WRITER и CHANNEL_URL_EDITOR в переменных окружения!")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))     # доп. команда на всякий
    app.add_handler(MessageHandler(filters.ALL, any_message))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
