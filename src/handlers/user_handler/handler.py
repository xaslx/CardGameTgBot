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



router: Router = Router(name='user handler')


@router.message(CommandStart(), StateFilter(default_state))
async def start_cmd(message: Message, session: AsyncSession):
    await message.answer(
        text=LEXICON_RU['/start']
    )
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)
    if not user:
        new_user: UserCreate = UserCreate(user_id=message.from_user.id)
        await UserRepository.add(session=session, **new_user.model_dump())
    


@router.message(Command('rules'), StateFilter(default_state))
async def get_rules(message: Message):
    await message.answer(
        text=LEXICON_RU['/rules']
    )



@router.message(Command('play'), StateFilter(default_state))
async def start_game(message: Message, state: FSMContext):
    await message.answer(text='Игра началась')
    await state.set_state(Game.play)


@router.message(StateFilter(Game.play))
async def game(message: Message):
    random_pairs = random.sample(list(CARDS_RU.items()), 2)
    my_cards = dict(random_pairs)
    

    await message.answer(
        text=
        f'Ваши карты:  <b>{", ".join(key for key in my_cards.keys())}</b>\n\n'
        f'Ваши очки: {sum(i for i in my_cards.values())}'
    )
        