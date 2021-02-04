import aiosqlite
from aiogram.types import CallbackQuery
from loader import dp


@dp.callback_query_handler(text='all_del_db')
async def save_db(call: CallbackQuery,):
    async with aiosqlite.connect('data/test.sql') as conn:
        await conn.execute('''DELETE FROM firms''')
        await conn.commit()
    await call.message.answer(text='Данные из СУДБ были успешно удалены')
