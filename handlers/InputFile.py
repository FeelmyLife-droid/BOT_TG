import os

from aiogram import types

from Keyboards.inline.inline_insert_db import key_insert_db_file
from data.config import BASE_DIR
from loader import dp, bot
from met import convert_docx_to_pdf
from met import convert_jpg_to_tiff
from met import convert_pdf_to_tiff
from met import main


@dp.message_handler(content_types=["document"])
async def handle_docs_audio(message: types.Message):
    print(message)
    for file in os.listdir(os.path.join(BASE_DIR, 'TEMP')):
        os.remove(os.path.join(BASE_DIR, 'TEMP', file))
    content = ''
    file = await bot.get_file(message.document.file_id)
    file_write = os.path.join(BASE_DIR, 'excel',
                              message.document.file_name)  # /Users/qeqe/Desktop/Натив/tele-bot/excel/АРАКУЛ.docx

    await bot.download_file(file.file_path, file_write)
    if os.path.exists(file_write):
        if os.path.exists(file_write):
            if message.document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                await main()
            elif message.document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                await convert_docx_to_pdf.to_tiff(message.document.file_name)

            elif message.document.mime_type == 'application/pdf':
                await convert_pdf_to_tiff.pdf_to_tiff(message.document.file_name, message.chat.id)

            elif message.document.mime_type == 'image/jpeg' or 'image/png':
                content = await convert_jpg_to_tiff._to_tiff(message.document.file_name)

            elif message.document.mime_type == 'text/plain':
                with open(file_write, 'r') as f:
                    count = len(f.readlines())
                    await message.reply(text=f'<b>В файле:{message.document.file_name}</b>\n {count} фирмы',
                                        reply_markup=key_insert_db_file)
    if len(content) != 0:
        doc = open(content, 'rb')
        await message.answer_document(doc)