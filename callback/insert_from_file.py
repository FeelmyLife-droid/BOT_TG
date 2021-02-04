import aiofiles
import aiosqlite
from aiogram.types import CallbackQuery
from data.config import BASE_DIR
from loader import dp
from Keyboards.inline.inline_check_db import key_check_db


@dp.callback_query_handler(text='insert_from_file')
async def inser_from_file(call: CallbackQuery):
    file_name = call.message.reply_to_message.document.file_name
    firms = []

    async with aiofiles.open(f'{BASE_DIR}/excel/{file_name}', 'r') as f:
        async for firm in f:
            firms.append(firm.rstrip())
    async with aiosqlite.connect('data/test.sql') as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS firms("
                           "ИНН BLOB NOT NULL)")
        cur = await conn.execute("SELECT ИНН FROM firms")
        for firm in firms:
            if await cur.fetchone() is None:
                await conn.execute('''INSERT INTO firms(ИНН) VALUES(?)''', (firm,))
                await conn.commit()

    await call.message.answer(f'Объекты успешно добавлены в СУБД', reply_markup=key_check_db)
