from aiogram.types import ReplyKeyboardMarkup, KeyboardButton





def get_keyboard() -> ReplyKeyboardMarkup:
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Взять ещё 🃏')],
            [KeyboardButton(text='Хватит 🫸')],
            [KeyboardButton(text='Отменить игру ⛔️')]
        ],
        resize_keyboard=True
    )
    return keyboard


def game_mode_with_player() -> ReplyKeyboardMarkup:
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Играть со ставкой 💸')],
            [KeyboardButton(text='Играть без ставки 🤝')],
            [KeyboardButton(text='Главное меню 💡')]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_kb_main_menu() -> ReplyKeyboardMarkup:
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Играть ▶️'), KeyboardButton(text='Мой профиль 📊')],
            [KeyboardButton(text='Таблица лидеров 🏆'), KeyboardButton(text='Получить бонус 🎁')],
            [KeyboardButton(text='Правила ❓')]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_mode_game() -> ReplyKeyboardMarkup:
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Играть с ботом 🤖')],
            [KeyboardButton(text='Играть с игроками 🧑‍💻')],
            [KeyboardButton(text='Главное меню 💡')]
        ],
        resize_keyboard=True
    )
    return keyboard