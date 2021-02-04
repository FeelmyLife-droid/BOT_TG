import aiosqlite
from aiogram import types

from Keyboards.inline.inline_keyb_func_db import key_func_db
from loader import dp


@dp.callback_query_handler(text='call_check_db')
async def call_inn(call: types.CallbackQuery):
    async with aiosqlite.connect('data/test.sql') as conn:
        cursor = await conn.execute('''SELECT ИНН FROM firms''')
        rows = await cursor.fetchall()
        inn = []
        for row in rows:
            inn.append(row[0])
        await call.message.answer(text=f'<b>В базе СУБД сейчас {len(inn)} объектов:</b>\n\n '+
                                  str(',\n'.join(str(i) for i in inn if i is not None)),reply_markup=key_func_db)
