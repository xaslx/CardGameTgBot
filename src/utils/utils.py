from src.lexicon.lexicon_ru import CARDS_RU
import random
from src.models.user import User
import random


def get_random_cards(k: int, cards: list) -> dict:
    random.shuffle(cards)
    random_cards = random.choices(cards, k=k)

    for card in random_cards:
        cards.remove(card)

    total_score: int = sum(CARDS_RU[i] for i in random_cards)
    return random_cards, total_score, cards






def get_my_profile(user: User) -> str:

    text: str = f'********************************\n' \
                f'<b>⚡️ Ваш профиль ⚡️</b>\n'  \
                f'********************************\n\n' \
                f'--------------------------------\n' \
                f'<b>🌟 Рейтинг: {user.rating}</b>\n' \
                f'--------------------------------\n' \
                f'<b>💰 Монет: {user.money}</b>\n' \
                f'--------------------------------\n' \
                f'<b>🥇 Побед: {user.wins}</b>\n' \
                f'--------------------------------\n' \
                f'<b>😾 Проигрышей: {user.losses}</b>\n' \
                f'--------------------------------\n' \
                f'<b>🎮 Игр сыграно: {user.games}</b>\n' \
                f'--------------------------------\n' \
                f'<b>🤝 Ничья: {user.draw}</b>\n' \
                f'--------------------------------\n'
    return text




def wins_lose_draw(my_cards: list, my_score: int, bot_cards: list, bot_score: int) -> str:
    text: str = (
        f'Карты бота: <b>{", ".join(bot_cards)}</b>\n'
        f'Очки бота: <b>{bot_score}</b>\n'
        f'---------------------------------------\n'
        f'Ваши карты: <b>{", ".join(my_cards)}</b>\n'
        f'Ваши очки: <b>{my_score}</b>\n'
        f'---------------------------------------\n'
    )
    
    return text
