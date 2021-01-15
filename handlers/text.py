import os
from asyncio.tasks import shield

from aiogram import types

from loader import dp, bot
from met import async_rus
from data.config import BASE_DIR


@dp.message_handler(text="Новые адреса")
async def new_adr(message: types.Message):
    file_path = str(async_rus.get_date()[1] + ' ' + async_rus.get_date()[0]) + '.xlsx'
    reply_text = f"Фирм зарегистрированные за {file_path.split('.')[0]}"
    if os.path.exists(os.path.join(BASE_DIR, 'excel', file_path)):
        doc = open(os.path.join(BASE_DIR, 'excel', file_path), 'rb')

    else:
        await shield(async_rus.main())
        doc = open(os.path.join(BASE_DIR, 'excel', file_path), 'rb')

    await bot.send_document(message.chat.id, doc)
    await message.answer(reply_text)
