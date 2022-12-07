import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
from handlers import api_requests, commands
from states import Task

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_PATH = ''
WEBHOOK_URL = 'https://db55-217-72-11-58.ngrok.io'  # ngrok link
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = '5000'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def register_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(
        commands.start,
        commands='start',
    )
    dp.register_message_handler(
        commands.cancel,
        commands='cancel',
    )
    dp.register_message_handler(
        commands.help,
        commands='help'
    )
    dp.register_message_handler(
        commands.add,
        commands='add',
    )
    dp.register_message_handler(
        commands.add,
        Text(equals='Добавить задачу', ignore_case=True)
    )


def register_api_requests_handlers(dp: Dispatcher):
    dp.register_message_handler(
        api_requests.response_to_add,
        state=Task.add_task,
    )
    dp.register_message_handler(
        api_requests.list,
        commands='list'
    )
    dp.register_message_handler(
        api_requests.list,
        Text(equals='Показать задачи', ignore_case=True)
    )
    dp.register_callback_query_handler(
        api_requests.delete_task,
        text='delete',
    )


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/help', description='Помощь'),
        BotCommand(command='/add', description='Добавить запись'),
        BotCommand(command='/list', description='Показать все записи'),
        BotCommand(command='/cancel', description='Отменяет добавление задачи')
    ]
    await bot.set_my_commands(commands)


async def on_startup(dp: Dispatcher):
    register_api_requests_handlers(dp)
    register_commands_handlers(dp)
    await set_commands(bot)
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp: Dispatcher):
    await bot.delete_webhook()


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
