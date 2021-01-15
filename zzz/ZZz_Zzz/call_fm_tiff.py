import os
import tempfile

from aiogram import types
from pdf2image import convert_from_path

from excel import BASE_DIR
from loader import dp, bot


@dp.callback_query_handler(text='fm_tiff')
async def call_fm_tiff(call: types.CallbackQuery):
    name_file = call.message.text.split('\n')[1].split('.')[0] + '.pdf'
    path_file_pdf = f'{BASE_DIR}/excel/{name_file}'
    if os.path.exists(f'excel/{name_file}'):
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                path_file_pdf,
                output_folder=path,
                last_page=1,
                dpi=300,
                first_page=0,
                grayscale=True
            )
        base_filename = os.path.splitext(os.path.basename(path_file_pdf))[0] + '.tiff'
        for page in images_from_path:
            page.save(os.path.join(BASE_DIR+'/excel', base_filename), 'JPEG')
        if os.path.exists(f'excel/{base_filename}'):
            doc_tiff = open(f'excel/{base_filename}', 'rb')
            await bot.send_document(call.from_user.id, doc_tiff)
