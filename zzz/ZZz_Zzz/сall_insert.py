import aiosqlite
from aiogram.types import CallbackQuery

from loader import dp
from temp import Info


@dp.callback_query_handler(text='insert')
async def call_insert(call: CallbackQuery):
    inn = Info(call.message.text).slovo

    await call.message.answer(inn)
    async with aiosqlite.connect('data/test.sql') as db:
        async with db.execute(f'''SELECT * FROM test WHERE ИНН={inn}''') as cur:
            firm = await cur.fetchone()
            if firm:
                await call.message.answer(f'{firm[0][:-1:]} уже есть в списке на проверку')
            else:
                c = Info(call.message.text).slovo
                print(c)
                await call.message.answer(f'такого {inn} нет')

        await cur.close()
        await db.close()
