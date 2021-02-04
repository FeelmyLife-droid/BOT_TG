import os

from aiogram import types
from zzz.ZZz_Zzz import async_write
from excel import BASE_DIR
from loader import dp, bot


@dp.callback_query_handler(text='fm_xlsx')
async def call_fm_xlsx(call: types.CallbackQuery):
    name_file = call.message.reply_to_message.document.file_name
    path = f'{BASE_DIR}/excel/{name_file}'
    if os.path.exists(f'excel/{name_file}'):
        doc_name = await async_write.main(path)
        doc_path = open(f'{BASE_DIR}/excel/{doc_name}', 'rb')
        await bot.send_document(call.from_user.id, doc_path)
