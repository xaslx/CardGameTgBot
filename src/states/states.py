from aiogram.fsm.state import State, StatesGroup


class Game(StatesGroup):
    play: State = State()