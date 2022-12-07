from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

delete = InlineKeyboardButton(text='Удалить', callback_data='delete')
delete_keyboard = InlineKeyboardMarkup()
delete_keyboard.add(delete)


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_buttons = [
    KeyboardButton(text='Добавить задачу'),
    KeyboardButton(text='Показать задачи')
]
start_keyboard.add(*start_buttons)
