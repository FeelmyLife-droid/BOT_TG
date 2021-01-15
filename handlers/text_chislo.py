from aiogram import types

from Keyboards.inline.key_inline import key_inline
from loader import dp


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    if message.text.isdigit() and len(message.text) == 10:
        await message.reply(text='Выберите действие', reply_markup=await key_inline(message.text))

