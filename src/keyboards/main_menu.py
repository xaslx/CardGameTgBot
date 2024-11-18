from aiogram import Bot
from aiogram.types import BotCommand
from config import env_config


bot: Bot = Bot(token=env_config.TOKEN_BOT)

async def set_main_menu():

    main_menu_commands = [
        BotCommand(command="/start", description="Главное меню 💡"),
        BotCommand(command="/play", description="Играть ▶️"),
        BotCommand(command="/profile", description="Мой профиль 📊"),
        BotCommand(command="/leadership", description="Таблица лидеров 🏆"),
        BotCommand(command="/rules", description="Правила ❓"),
        BotCommand(command="/bonus", description="Получить бонус 🎁"),
        BotCommand(command="/cancel", description="Отменить игру ⛔️"),
    ]

    await bot.set_my_commands(main_menu_commands)