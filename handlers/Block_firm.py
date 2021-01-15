import aiosqlite

from Keyboards.inline.inline_keyb_func_db import key_func_db
from loader import dp
from aiogram import types
from data.config import BASE_DIR
import os


@dp.message_handler(text='Блокировка Фирм')
async def block_firm(message: types.Message):
    async with aiosqlite.connect(os.path.join(BASE_DIR, 'data','test.sql' )) as conn:
        cursor = await conn.execute('''SELECT ИНН FROM firms''')
        rows = await cursor.fetchall()
        inn = []
        for row in rows:
            inn.append(row[0])
        if len(inn) == 0:
            await message.answer(text=f'<b>В базе СУБД сейчас {len(inn)} объектов:\n\n\n</b> Если необходимо добавить '
                                      f'данные в базу для проверки. Просто пришлите текстовый файл с расширением '
                                      f'"TXT"')
        else:
            await message.answer(text=f'<b>В базе СУБД сейчас {len(inn)} объектов:</b>\n\n ' +
                                      str(',\n'.join(str(i) for i in inn if i is not None)),
                                 reply_markup=key_func_db)
