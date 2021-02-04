import os

from aiogram import types
from excel import BASE_DIR
from loader import dp, bot
import subprocess

from zzz.ZZz_Zzz import async_write


@dp.callback_query_handler(text='fm_pdf')
async def call_fm_pdf(call: types.CallbackQuery):
    name_file = call.message.reply_to_message.document.file_name
    path = f'{BASE_DIR}/excel/{name_file}'
    if os.path.exists(f'excel/{name_file}'):
        doc_name = await async_write.main(path)
        doc_new = f'"{BASE_DIR}/excel/{doc_name}"'
        subprocess.run([f'unoconv -f pdf {doc_new}'], shell=True)
        file_pdf = doc_name.split('.')[0] + '.pdf'
        if os.path.exists(f'excel/{file_pdf}'):
            f = open(f'excel/{file_pdf}', 'rb')
            await bot.send_document(call.from_user.id, f)
