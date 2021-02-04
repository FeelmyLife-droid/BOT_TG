import aiosqlite
from aiogram import types

from loader import dp


@dp.callback_query_handler(callable('add'))
async def call_inn(call: types.CallbackQuery):
    if call.data == 'add':  # Ошибка 'ValueError: no active connection' надо исправить
        info = []
        i = call.message.text.split('\n')
        for n in i:
            k = n.split(":")
            info.append(str(k[1]))
        async with aiosqlite.connect('test.sql') as db:
            cursor = await db.execute('''CREATE TABLE IF NOT EXISTS test(
                Название TEXT NOT NULL,
                ОГРН INTEGER NOT NULL,
                ИНН INTEGER NOT NULL,
                Регион TEXT,
                Адресс TEXT,
                Директор TEXT,
                ОКВЭД TEXT,
                Уставной капилал INTEGER NOT NULL,
                Дата_рег TEXT)''')
            await cursor.close()
            await db.close()
        async with aiosqlite.connect('test.sql') as conn:
            await conn.execute(f'''INSERT INTO test VALUES (?,?,?,?,?,?,?,?,?);''', info)
            await conn.commit()
            await conn.close()
        await call.answer(f'')