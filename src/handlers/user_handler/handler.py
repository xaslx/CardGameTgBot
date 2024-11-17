from typing import Any
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.lexicon.lexicon_ru import LEXICON_RU, CARDS_RU
from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UserCreate
import random
from src.states.states import Game
from src.keyboards.user_keyboards.keyboards import get_keyboard, get_kb_main_menu
from src.utils.utils import get_random_cards, get_my_cards_and_points, get_my_profile



router: Router = Router(name='user handler')


@router.message(CommandStart(), StateFilter(default_state))
async def start_cmd(message: Message, session: AsyncSession):
    await message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=get_kb_main_menu()
    )
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)
    if not user:
        new_user: UserCreate = UserCreate(user_id=message.from_user.id)
        await UserRepository.add(session=session, **new_user.model_dump())
    


@router.message(StateFilter(default_state), (F.text == 'Правила ❓') | (F.text == '/rules'))
async def get_rules(message: Message):
    await message.answer(
        text=LEXICON_RU['/rules']
    )


@router.message(StateFilter(default_state), (F.text == 'Мой профиль 📊') | (F.text == '/profile'))
async def my_profile(message: Message, session: AsyncSession):
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)
    if user:
        text: str = get_my_profile(user=user)
        return await message.answer(text=text)


@router.message(StateFilter(default_state), (F.text == 'Играть ▶️') | (F.text == '/play'))
async def start_game(message: Message, state: FSMContext):
    pass