import aiosqlite
from aiogram.types import CallbackQuery

from loader import dp
from temp import Info


@dp.callback_query_handler(text='insert')
async def call_insert(call: CallbackQuery):
    inn = call.message.text.split('\n')[2].split(":")[1].strip()
    await call.message.answer(inn)
    async with aiosqlite.connect('data/test.sql') as db:
        async with db.execute(f'''SELECT * FROM test WHERE ИНН={inn}''') as cur:
            firm = await cur.fetchone()
            if firm:
                await call.message.answer(f'{firm[0][:-1:]} уже есть в списке на проверку')
            else:
                c = Info(call.message.text)
                print(c.name)
                await call.message.answer(f'такого {inn} нет')

        await cur.close()
        await db.close()
