import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_ЗДЕСЬ")
ADMIN_USERNAME = "@fedor_merzlikin"

# ===== 10 БИЛЕТОВ =====
TICKETS = [
    {
        "num": 1,
        "question": "Знак «Стоянка запрещена» означает:",
        "options": [
            "A) Нельзя ни стоять, ни останавливаться",
            "B) Нельзя стоять, но можно остановиться ✅",
            "C) Нельзя останавливаться, но можно стоять",
        ],
        "answer": "B",
        "explanation": "⚡️ Стоянка запрещена (синий круг с одной линией) — стоять нельзя, но кратковременная остановка разрешена. Путают со знаком «Остановка запрещена» (синий круг с крестом) — там нельзя вообще ничего."
    },
    {
        "num": 2,
        "question": "Водитель должен уступить дорогу пешеходу на нерегулируемом пешеходном переходе:",
        "options": [
            "A) Только если пешеход уже вышел на проезжую часть",
            "B) Только если пешеход идёт прямо перед машиной",
            "C) Если пешеход вступил на проезжую часть или обозначил намерение перейти ✅",
        ],
        "answer": "C",
        "explanation": "⚡️ Достаточно того, что пешеход только собирается переходить — уже нужно уступить. Не ждите пока он выйдет под колёса."
    },
    {
        "num": 3,
        "question": "Обгон запрещён:",
        "options": [
            "A) На мосту ✅",
            "B) На прямом участке дороги",
            "C) За городом",
        ],
        "answer": "A",
        "explanation": "⚡️ Обгон запрещён на мостах, путепроводах, эстакадах и под ними, в тоннелях, на ж/д переездах и 100м до них, на перекрёстках, в конце подъёма и на опасных поворотах."
    },
    {
        "num": 4,
        "question": "При повороте налево водитель должен уступить дорогу:",
        "options": [
            "A) Только пешеходам",
            "B) Встречным ТС и пешеходам ✅",
            "C) Только встречным автомобилям",
        ],
        "answer": "B",
        "explanation": "⚡️ При повороте налево уступаем встречному транспорту и пешеходам, переходящим дорогу. При повороте направо — только пешеходам."
    },
    {
        "num": 5,
        "question": "Что означает мигающий жёлтый сигнал светофора?",
        "options": [
            "A) Движение запрещено",
            "B) Нерегулируемый перекрёсток, будьте внимательны ✅",
            "C) Можно ехать без ограничений",
        ],
        "answer": "B",
        "explanation": "⚡️ Мигающий жёлтый = светофор не работает в штатном режиме. Перекрёсток считается нерегулируемым — действуют правила приоритета (помеха справа и знаки)."
    },
    {
        "num": 6,
        "question": "На каком расстоянии до ж/д переезда запрещён обгон?",
        "options": [
            "A) 50 метров",
            "B) 200 метров",
            "C) 100 метров ✅",
        ],
        "answer": "C",
        "explanation": "⚡️ За 100 метров до ж/д переезда обгон запрещён. Это одна из самых частых ловушек в билетах — путают с 50м и 200м."
    },
    {
        "num": 7,
        "question": "Минимальная скорость на автомагистрали:",
        "options": [
            "A) 40 км/ч ✅",
            "B) 60 км/ч",
            "C) Не установлена",
        ],
        "answer": "A",
        "explanation": "⚡️ На автомагистрали нельзя ехать медленнее 40 км/ч (кроме случаев когда это невозможно по техническим причинам). Максимальная — 110 км/ч."
    },
    {
        "num": 8,
        "question": "Знак «Главная дорога» имеет форму:",
        "options": [
            "A) Круга с красной рамкой",
            "B) Жёлтого ромба с белой рамкой ✅",
            "C) Треугольника с красной рамкой",
        ],
        "answer": "B",
        "explanation": "⚡️ Главная дорога — жёлтый ромб. Конец главной дороги — тот же ромб, но с чёрной диагональной полосой поверх. Не путайте!"
    },
    {
        "num": 9,
        "question": "При движении задним ходом водитель:",
        "options": [
            "A) Имеет преимущество перед всеми",
            "B) Должен уступить всем участникам движения ✅",
            "C) Имеет преимущество только перед пешеходами",
        ],
        "answer": "B",
        "explanation": "⚡️ При движении задним ходом — уступаем всем. И не забывайте: задним ходом запрещено движение на перекрёстках, пешеходных переходах, в тоннелях, на мостах и ж/д переездах."
    },
    {
        "num": 10,
        "question": "В каком случае можно пересечь сплошную линию разметки?",
        "options": [
            "A) Для объезда препятствия если нет другой возможности ✅",
            "B) Никогда нельзя",
            "C) Если едешь быстрее попутного транспорта",
        ],
        "answer": "A",
        "explanation": "⚡️ Сплошную можно пересечь только для объезда препятствия (не медленно едущего авто!) если объехать иначе невозможно. При этом нужно убедиться в безопасности манёвра."
    },
]


# ===== HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("📋 Получить 10 билетов", callback_data="ticket_1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"🚗 *Прямая Дорога* — подготовка к теории ПДД\n\n"
        f"Я пришлю тебе *10 билетов* на которых чаще всего ошибаются на экзамене.\n\n"
        f"Разберём каждый вопрос с объяснением — почему именно этот ответ правильный.\n\n"
        f"Поехали? 👇",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def send_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("ticket_"):
        num = int(data.split("_")[1])

        if num > len(TICKETS):
            await send_final_offer(query)
            return

        ticket = TICKETS[num - 1]
        options_text = "\n".join(ticket["options"])

        keyboard = [
            [InlineKeyboardButton("✅ Показать ответ", callback_data=f"answer_{num}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            f"*Билет {num} из {len(TICKETS)}*\n\n"
            f"❓ {ticket['question']}\n\n"
            f"{options_text}",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif data.startswith("answer_"):
        num = int(data.split("_")[1])
        ticket = TICKETS[num - 1]
        next_num = num + 1

        if next_num <= len(TICKETS):
            keyboard = [[InlineKeyboardButton(f"Следующий билет {next_num} →", callback_data=f"ticket_{next_num}")]]
        else:
            keyboard = [[InlineKeyboardButton("🎯 Узнать про полный курс", callback_data="offer")]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            f"*Правильный ответ: {ticket['answer']}*\n\n"
            f"{ticket['explanation']}",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif data == "offer":
        await send_final_offer(query)


async def send_final_offer(query):
    keyboard = [
        [InlineKeyboardButton("💳 Хочу полный курс", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "🎉 *Молодец, прошёл все 10 билетов!*\n\n"
        "Это только малая часть того что спрашивают на экзамене.\n\n"
        "📚 *Полный курс «Прямая Дорога»* — это:\n"
        "• Разбор всех билетов по темам\n"
        "• Объяснение каждой ловушки\n"
        "• Только важное, без воды\n\n"
        "💰 *Стоимость: 1990₽*\n\n"
        "Напиши мне — расскажу как получить доступ 👇",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(send_ticket))
    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
