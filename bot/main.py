import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook
import handlers


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_PATH = '/'
WEBHOOK_URL = 'https://ae55-217-72-11-58.ngrok.io'  # ngrok link
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = '5000'

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        handlers.start,
        commands='/start',
    )


def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/help', description='Помощь'),
        BotCommand(command='/add', description='Добавить запись'),
        BotCommand(command='/list', description='Показать все записи'),
    ]
    bot.set_my_commands(commands)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp: Dispatcher):
    await bot.delete_webhook()


if __name__ == '__main__':
    register_handlers(dp)
    set_commands(bot)

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
