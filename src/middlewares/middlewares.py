from typing import Callable, Dict, Any, Awaitable
 
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.models.user import User
from src.repositories.user import UserRepository



class UserCheckMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker):
        self.factory = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id: int = event.event.chat.id

        async with self.factory() as session:
            user: User = await UserRepository.find_one_or_none(session=session, user_id=user_id)

            if user is None:
                await UserRepository.add(session=session, user_id=user_id, name=event.event.chat.first_name)
                return

            if user.name != event.event.chat.first_name:
                await UserRepository.update(session=session, id=user.id, name=event.event.chat.first_name) 

            data['user'] = user
            return await handler(event, data)



class DbMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker):
        self.factory = session_factory
 
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.factory() as session:
            data['session'] = session
            return await handler(event, data)