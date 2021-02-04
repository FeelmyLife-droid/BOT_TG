from aiogram import types

from loader import dp


@dp.message_handler(commands='help')
async def help_cmd_handler(message: types.Message):
    await message.answer(f"Привет <b>{message.chat.first_name}</b>!\n"
                         f"Нужна помошь?\n"
                         f'Для преобрадования <b>DOCX в TIFF:</b>\n <b>ВАЖНО НАЗВАНИЕ ФАЙЛА "ПРИМЕР.DOCX" ОДНИМ СЛОВОМ</b>')