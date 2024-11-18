import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import env_config
from src.middlewares.middlewares import DbMiddleware, UserCheckMiddleware
from database import async_session_maker
from src.handlers.user_handler.handler import router as user_router


logger = logging.getLogger(__name__)



async def on_startup():
    logger.info('Бот включен')
    

async def on_shutdown():
    logger.info('Бот выключен')



async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    bot: Bot = Bot(token=env_config.TOKEN_BOT, default=DefaultBotProperties(parse_mode='HTML'))
    dp: Dispatcher = Dispatcher()
    dp.update.middleware.register(DbMiddleware(async_session_maker))
    dp.update.middleware.register(UserCheckMiddleware(async_session_maker))
    dp.include_router(user_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")