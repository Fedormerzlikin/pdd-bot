import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_ЗДЕСЬ")
CHANNEL_URL = "https://t.me/pddteoria"
ADMIN_USERNAME = "@fedor_merzlikin"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ Принимаю условия", callback_data="accept")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "⚠️ *Перед началом ознакомьтесь с условиями*\n\n"
        "Материалы данного бота и канала являются *информационно-справочными* и предназначены исключительно для самостоятельной подготовки к экзамену по ПДД.\n\n"
        "Нажимая кнопку ниже, вы подтверждаете что:\n\n"
        "• Материалы *не являются образовательной услугой*\n"
        "• Бот не является автошколой и не выдаёт документов\n"
        "• Данное взаимодействие *не является публичной офертой*\n"
        "• Вы используете материалы на своё усмотрение\n\n"
        "Продолжая, вы соглашаетесь с вышеизложенным.",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "accept":
        keyboard = [
            [InlineKeyboardButton("📚 Перейти на канал с материалами", url=CHANNEL_URL)],
            [InlineKeyboardButton("💳 Купить полный курс", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            f"Отлично! 🚗\n\n"
            f"*Прямая Дорога* — подготовка к теории ПДД\n\n"
            f"На канале тебя ждут:\n"
            f"• Разбор билетов на которых чаще всего ошибаются\n"
            f"• Знаки ПДД которые путают все\n"
            f"• Ловушки на экзамене\n\n"
            f"Переходи и подписывайся 👇",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
