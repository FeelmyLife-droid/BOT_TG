from aiogram.types import CallbackQuery
from loader import dp


@dp.callback_query_handler(text='save_db')
async def save_db(call: CallbackQuery):
    await call.message.answer(text='Данные успешно сохранены')
