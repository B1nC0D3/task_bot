from aiogram.types import Message


async def add(message: Message):
    pass


async def list(message: Message):
    pass


async def start(message: Message):
    await message.answer(
        'Это бот-органайзер, для добавления задачи используйте команду /add, '
        'для просмотра смоих задач - /list. '
        'Ограничение 5 задач на пользователя')


async def blank(message: Message):
    pass
