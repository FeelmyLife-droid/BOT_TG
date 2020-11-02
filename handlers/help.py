from aiogram import types

from loader import dp


@dp.message_handler(commands='help')
async def help_cmd_handler(message: types.Message):
    await message.answer(f"Привет <b>{message.chat.first_name}</b>!\nНужна помошь?")