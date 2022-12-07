from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, HTTPException, status

from bot.main import (WEBHOOK_URL, bot, dp, register_api_requests_handlers,
                      register_commands_handlers, set_commands)
from database import Task, session

app = FastAPI()
TASK_PER_USER = 5


@app.post('/add')
async def add_task(user_id: int, message: str) -> dict:
    tasks_amount = session.query(Task).filter(Task.user_id == user_id).count()
    if tasks_amount >= TASK_PER_USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя создать больше 5 записей'
        )
    try:
        new_task = Task(
            user_id=user_id,
            description=message,
        )
        session.add(new_task)
        session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Не удалось создать задачу'
        )
    return {
        'detail': 'Задача добавлена'
    }


@app.delete('/add')
async def delete_task(user_id: int, message: str) -> dict:
    try:
        task_to_delete = session.query(Task).filter(
            Task.user_id == user_id and Task.description == message).first()
        session.delete(task_to_delete)
        session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Не удалось удалить задачу'
        )
    return {
        'detail': 'Задача удалена'
    }


@app.get('/list')
async def get_tasks(user_id: int):
    try:
        tasks = session.query(
            Task.description).filter(Task.user_id == user_id).all()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Не удалось получить задачи'
        )
    return {
        'detail': tasks
    }


@app.on_event('startup')
async def on_startup():
    register_api_requests_handlers(dp)
    register_commands_handlers(dp)
    await set_commands()
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event('shutdown')
async def on_shutdown():
    await bot.delete_webhook()


@app.post('/')
async def bot_webhook(update: dict):
    telegram_update = Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
