from aiogram import types

from Keyboards.default.key_start import key_start
from loader import dp


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.answer(f"Привет <b>{message.chat.first_name}</b>!\nНачнем?", reply_markup=key_start)
