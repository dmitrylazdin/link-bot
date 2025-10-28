import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")           # зададим в Railway
CHANNEL_URL = os.getenv("CHANNEL_URL")       # зададим в Railway
LINK_BUTTON_TEXT = "Перейти в канал"

def link_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton(LINK_BUTTON_TEXT, url=CHANNEL_URL)]])

async def send_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ("Подробная информация о  вакансии копирайтера сценариев описана по ссылке 👇\n\n"
            "Если кнопка не открылась, используйте прямую ссылку:\n"
            f"{CHANNEL_URL}")
    await update.effective_chat.send_message(
        text, reply_markup=link_keyboard(),
        disable_web_page_preview=True, parse_mode=ParseMode.HTML
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_link(update, context)

def main():
    if not BOT_TOKEN or not CHANNEL_URL:
        raise RuntimeError("Укажите BOT_TOKEN и CHANNEL_URL в переменных окружения!")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("link", start))
    app.add_handler(MessageHandler(filters.ALL, send_link))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
