from aiogram.types import ReplyKeyboardMarkup, KeyboardButton





def get_keyboard() -> ReplyKeyboardMarkup:
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Взять ещё 🃏')],
            [KeyboardButton(text='Хватит 🫸')]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_kb_main_menu() -> ReplyKeyboardMarkup:
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Играть ▶️')],
            [KeyboardButton(text='Мой профиль 📊')],
            [KeyboardButton(text='Правила ❓')]
        ],
        resize_keyboard=True
    )
    return keyboard