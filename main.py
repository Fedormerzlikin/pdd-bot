import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_ЗДЕСЬ")
ADMIN_USERNAME = "@fedor_merzlikin"

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
        "explanation": "⚡️ Стоянка запрещена (синий круг с одной линией) — стоять нельзя, но кратковременная остановка разрешена. Путают со знаком «Остановка запрещена» (синий круг с крестом) — там нельзя вообще ничего.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Russian_road_sign_3.28.svg/240px-Russian_road_sign_3.28.svg.png"
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
        "explanation": "⚡️ Достаточно того, что пешеход только собирается переходить — уже нужно уступить. Не ждите пока он выйдет под колёса.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Russian_road_sign_5.19.1.svg/240px-Russian_road_sign_5.19.1.svg.png"
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
        "explanation": "⚡️ Обгон запрещён на мостах, путепроводах, эстакадах и под ними, в тоннелях, на ж/д переездах и 100м до них, на перекрёстках, в конце подъёма и на опасных поворотах.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Russian_road_sign_3.20.svg/240px-Russian_road_sign_3.20.svg.png"
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
        "explanation": "⚡️ При повороте налево уступаем встречному транспорту и пешеходам, переходящим дорогу. При повороте направо — только пешеходам.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Russian_road_sign_4.1.1.svg/240px-Russian_road_sign_4.1.1.svg.png"
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
        "explanation": "⚡️ Мигающий жёлтый = светофор не работает в штатном режиме. Перекрёсток считается нерегулируемым — действуют правила приоритета (помеха справа и знаки).",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Traffic_lights_3_states.svg/120px-Traffic_lights_3_states.svg.png"
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
        "explanation": "⚡️ За 100 метров до ж/д переезда обгон запрещён. Это одна из самых частых ловушек в билетах — путают с 50м и 200м.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Russian_road_sign_1.3.1.svg/240px-Russian_road_sign_1.3.1.svg.png"
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
        "explanation": "⚡️ На автомагистрали нельзя ехать медленнее 40 км/ч. Максимальная — 110 км/ч.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Russian_road_sign_5.1.svg/240px-Russian_road_sign_5.1.svg.png"
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
        "explanation": "⚡️ Главная дорога — жёлтый ромб. Конец главной дороги — тот же ромб, но с чёрной диагональной полосой поверх.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Russian_road_sign_2.1.svg/240px-Russian_road_sign_2.1.svg.png"
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
        "explanation": "⚡️ При движении задним ходом — уступаем всем. Задним ходом запрещено на перекрёстках, пешеходных переходах, в тоннелях, на мостах и ж/д переездах.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Russian_road_sign_3.38.svg/240px-Russian_road_sign_3.38.svg.png"
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
        "explanation": "⚡️ Сплошную можно пересечь только для объезда препятствия (не медленно едущего авто!) если объехать иначе невозможно.",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Zeichen_295.svg/240px-Zeichen_295.svg.png"
    },
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        "⚠️ *Важная информация*\n\n"
        "Этот бот предоставляет *информационные и справочные материалы* для самостоятельной подготовки к экзамену по теории ПДД.\n\n"
        "Материалы *не являются образовательной услугой* и не заменяют обучение в лицензированной автошколе. "
        "Используя этот бот, вы соглашаетесь с тем, что получаете справочную информацию, а не услуги обучения.",
        parse_mode="Markdown"
    )

    keyboard = [[InlineKeyboardButton("✅ Понял, поехали!", callback_data="ticket_1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"🚗 *Прямая Дорога* — подготовка к теории ПДД\n\n"
        f"Пришлю тебе *10 билетов* на которых чаще всего ошибаются на экзамене — с разбором каждого вопроса.\n\n"
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

        keyboard = [[InlineKeyboardButton("✅ Показать ответ", callback_data=f"answer_{num}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = (
            f"*Билет {num} из {len(TICKETS)}*\n\n"
            f"❓ {ticket['question']}\n\n"
            f"{options_text}"
        )

        if ticket.get("image_url"):
            try:
                await query.message.reply_photo(
                    photo=ticket["image_url"],
                    caption=text,
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )
            except Exception:
                await query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

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
