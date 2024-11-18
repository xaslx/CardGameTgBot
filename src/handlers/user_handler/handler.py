from sre_parse import State
from typing import Any
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.lexicon.lexicon_ru import LEXICON_RU, CARDS_RU, CARDS_SUIT, ALL_CARDS
from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UserCreate
import random
from src.states.states import Game
from src.keyboards.user_keyboards.keyboards import get_keyboard, get_kb_main_menu
from src.utils.utils import get_random_cards, get_my_profile, wins_lose_draw


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
    


@router.message(StateFilter(default_state), F.text.in_(['Правила ❓', '/rules']))
async def get_rules(message: Message):
    await message.answer(
        text=LEXICON_RU['/rules']
    )


@router.message(StateFilter(default_state), F.text.in_(['Мой профиль 📊', '/profile']))
async def my_profile(message: Message, session: AsyncSession):
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)
    if user:
        text: str = get_my_profile(user=user)
        return await message.answer(text=text)



@router.message(StateFilter(default_state), F.text.in_(['Играть ▶️', '/play']))
async def start_game(message: Message, state: FSMContext, session: AsyncSession):
    copy_cards: dict = ALL_CARDS.copy()
    my_cards, my_total_score, cards = get_random_cards(k=2, cards=copy_cards)
    bot_cards, bot_total_score, cards = get_random_cards(k=1, cards=copy_cards)
    

    await state.update_data({'cards': cards})
    await state.update_data(
        {'User': {'cards': my_cards, 'total_score': my_total_score}, 'Bot': {'cards': bot_cards, 'total_score': bot_total_score}}
    )

    data: dict = await state.get_data()
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)

    if all(card == 'Т' for card in data['User']['cards']):
        random_rating: int = random.randint(40, 70)
        
        await UserRepository.update(session=session, id=user.id, wins=user.wins + 1, games=user.games + 1, rating=user.rating + random_rating)
        return await message.answer(
            text='<b>Поздравляем! Вы Выиграли!\nВам выпало 2 туза - золотое очко</b>\n' + f'<b>Вам начислено {random_rating} рейтинга</b>',
            reply_markup=get_kb_main_menu()
        )
    
    if my_total_score == 21:
        random_rating: int = random.randint(40, 70)
        await UserRepository.update(session=session, id=user.id, wins=user.wins + 1, games=user.games + 1, raing=user.rating + random_rating)
        await state.clear()
        return await message.answer(
            text='<b>Вы Выиграли!</b>\n\n'
            f'<b>Ваши карты: {", ".join(my_cards)}</b>\n\n'
            f'<b>Ваши очки: {my_total_score}</b>\n\n'
            f'------------------------------------\n'
            f'<b>Вам начислено {random_rating} рейтинга</b>',
            reply_markup=get_kb_main_menu()
        )
    
    await message.answer(
        text=
        f'Ваши карты: <b>{", ".join(list(data['User']['cards']))}</b>\nВаши очки: {data['User']['total_score']}',
        reply_markup=get_keyboard()
    )

    await state.set_state(Game.play)    



@router.message(StateFilter(Game.play), F.text == 'Взять ещё 🃏')
async def game(message: Message, state: FSMContext, session: AsyncSession):
    data: dict = await state.get_data()
    new_card, total_score, cards = get_random_cards(k=1, cards=data['cards'])
    
    updated_cards = data['User']['cards'] + new_card
    my_total_score = data['User']['total_score'] + total_score
    
    await state.update_data({'User': {'cards': updated_cards, 'total_score': my_total_score}, 'cards': cards})
    random_rating: int = random.randint(40, 70)
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)

    if my_total_score > 21:
        await UserRepository.update(session=session, id=user.id, losses=user.losses + 1, games=user.games + 1)
        await state.clear()
        return await message.answer(
            text=
            '<b>Вы проиграли! У вас перебор</b>\n\n'
            f'<b>Ваши карты: {", ".join(updated_cards)}</b>\n\n'
            f'<b>Ваши очки: {my_total_score}</b>\n\n'
            f'------------------------------------\n'
            f'<b>Вы потеряли {random_rating} рейтинга</b>',
            reply_markup=get_kb_main_menu()
        )
    
    if my_total_score == 21:
        random_rating: int = random.randint(40, 70)
        await UserRepository.update(session=session, id=user.id, wins=user.wins + 1, games=user.games + 1, raing=user.rating + random_rating)
        await state.clear()
        return await message.answer(
            text='<b>Вы Выиграли!</b>\n\n'
            f'<b>Ваши карты: {", ".join(updated_cards)}</b>\n\n'
            f'<b>Ваши очки: {my_total_score}</b>\n\n'
            f'------------------------------------\n'
            f'<b>Вы потеряли {random_rating} рейтинга</b>',
            reply_markup=get_kb_main_menu()
        )

    await message.answer(
        text=f'Ваши карты: <b>{", ".join(updated_cards)}</b>\nВаши очки: {my_total_score}',
        reply_markup=get_keyboard()
    )



@router.message(StateFilter(Game.play), F.text == 'Хватит 🫸')
async def stop_game(message: Message, state: FSMContext, session: AsyncSession):
    user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)
    data: dict = await state.get_data()
    random_rating: int = random.randint(40, 70)
    my_cards, my_total_score = data['User']['cards'], data['User']['total_score']
    bot_cards: list = data['Bot']['cards']
    bot_total_score: int = data['Bot']['total_score']


    while bot_total_score <= 19:
        new_card, card_score, _ = get_random_cards(k=1, cards=data['cards'])
        bot_cards.extend(new_card)
        bot_total_score += card_score


    text: str = wins_lose_draw(my_cards=my_cards, my_score=my_total_score, bot_cards=bot_cards, bot_score=bot_total_score)
    await state.clear()

    if all(card == 'Т' for card in data['Bot']['cards']):
        random_rating: int = random.randint(40, 70)
        user: User = await UserRepository.find_one_or_none(session=session, user_id=message.from_user.id)
        await UserRepository.update(session=session, id=user.id, losses=user.wins + 1, games=user.games + 1, rating=user.rating - random_rating)
        return await message.answer(
            text='<b>Вы Проиграли!\nУ компьютера выпало 2 туза - золотое очко</b>\n' + f'<b>Вы потеряли {random_rating} рейтинга</b>',
            reply_markup=get_kb_main_menu()
        )

    if bot_total_score > 21:
        await UserRepository.update(session=session, id=user.id, wins=user.wins + 1, games=user.games + 1, rating=user.rating + random_rating)
        return await message.answer(
            text='<b>Поздравляем! Вы выиграли!</b>\n\n' + text + f'<b>Вам начислено {random_rating} рейтинга</b>',
            reply_markup=get_kb_main_menu()
        )

    if my_total_score > bot_total_score:
        await UserRepository.update(session=session, id=user.id, wins=user.wins + 1, games=user.games + 1, rating=user.rating + random_rating)
        return await message.answer(
            text='<b>Поздравляем! Вы выиграли!</b>\n\n' + text + f'<b>Вам начислено {random_rating} рейтинга</b>',
            reply_markup=get_kb_main_menu()
        )

    if my_total_score < bot_total_score:
        await UserRepository.update(session=session, id=user.id, losses=user.losses + 1, games=user.games + 1, rating=user.rating - random_rating)
        return await message.answer(
            text='<b>Вы проиграли!</b>\n\n' + text + f'<b>Вы потеряли {random_rating} рейтинга</b>',
            reply_markup=get_kb_main_menu()
        )

    if my_total_score == bot_total_score:
        await UserRepository.update(session=session, id=user.id, draw=user.draw + 1, games=user.games + 1, rating=user.rating + 10)
        return await message.answer(
            text='<b>Ничья</b>\n\n' + text + '<b>Вам начислено 10 рейтинга</b>',

            reply_markup=get_kb_main_menu()
        )
