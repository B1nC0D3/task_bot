from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from ..keys import start_keyboard
from ..states import Task


async def start(message: Message):
    await message.answer(
        'Это бот-органайзер, для добавления задачи используйте команду /add, '
        'для просмотра смоих задач - /list. '
        'Ограничение 5 задач на пользователя',
        reply_markup=start_keyboard)


async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено!')


async def help(message: Message):
    await message.answer(
        'Это бот-органайзер, для добавления задачи используйте команду /add, '
        'для просмотра смоих задач - /list. '
        'Ограничение 5 задач на пользователя')


async def add(message: Message, state: FSMContext):
    await message.answer('Введите описание задачи')
    await state.set_state(Task.add_task)
