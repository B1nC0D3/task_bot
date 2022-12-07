from http import HTTPStatus

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.client_reqrep import ClientResponse
from keys import delete_keyboard

API_ADDRESS = 'http://127.0.0.1:9000'


async def connect_to_url(
        url: str, request_type: str, params: tuple[tuple]) -> ClientResponse:
    url = API_ADDRESS + url
    async with ClientSession() as session:
        try:
            response = await session.__getattribute__(request_type)(
                url,
                params=params)
        except ClientConnectionError:
            raise ClientConnectionError('Не удалось подключиться к серверу')
        return response


async def response_to_add(message: Message, state: FSMContext):
    try:
        response = await connect_to_url(
            '/add',
            'post',
            params=(
                ('user_id', message.from_user.id),
                ('message', message.text)
            ))
    except ClientConnectionError as e:
        await message.answer(f'Произошла ошибка: {e}')
        await state.finish()
        return
    if response.content_type != 'application/json':
        await message.answer(
            f'Неизвестная ошибка, код ошибки: {response.status}'
        )
        return
    json_response = await response.json()
    detail = json_response.get('detail')
    if detail is None:
        detail = 'Неизвестная ошибка'
    if response.status != HTTPStatus.OK:
        await message.answer(
            'Ошибка \n'
            f'Код ошибки: {response.status} \n'
            f'Описание ошибки: {detail}')
        await state.finish()
        return
    await message.answer(detail)
    await state.finish()


async def list(message: Message):
    try:
        response = await connect_to_url(
            '/list',
            'get',
            params=(
                ('user_id', message.from_user.id),
            )
        )
    except ClientConnectionError as e:
        await message.answer(f'Произошла ошибка {e}')
        return
    if response.content_type != 'application/json':
        await message.answer(
            f'Неизвестная ошибка, код ошибки: {response.status}'
        )
        return
    json_response = await response.json()
    detail = json_response.get('detail')
    if detail is None:
        detail = 'Неизвестная ошибка'
    if response.status != HTTPStatus.OK:
        await message.answer(
            'Ошибка \n'
            f'Код ошибки: {response.status} \n'
            f'Описание ошибки: {detail}')
        return
    if len(detail) == 0:
        await message.answer('У вас нет запланированных задач')
        return
    await message.answer('Вот ваши задачи:')
    for description in detail:
        await message.answer(
            description.get('description'),
            reply_markup=delete_keyboard)


async def delete_task(call: CallbackQuery):
    try:
        response = await connect_to_url(
            '/add',
            'delete',
            params=(
                ('user_id', call.message.chat.id),
                ('message', call.message.text)
            )
        )
    except ClientConnectionError as e:
        await call.message.answer(f'Произошла ошибка {e}')
        return
    if response.content_type != 'application/json':
        await call.message.answer(
            f'Неизвестная ошибка, код ошибки: {response.status}'
        )
        return
    json_response = await response.json()
    detail = json_response.get('detail')
    if response.status != HTTPStatus.OK:
        await call.message.answer(
            'Ошибка \n'
            f'Код ошибки: {response.status} \n'
            f'Описание ошибки: {detail}')
        return
    await call.message.answer(detail)
    await call.message.delete()
    await call.answer()
