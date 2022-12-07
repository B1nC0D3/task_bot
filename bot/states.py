from aiogram.dispatcher.filters.state import State, StatesGroup


class Task(StatesGroup):
    add_task = State()
