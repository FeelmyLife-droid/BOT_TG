from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

key_func_db = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f'Сохарнить данные', callback_data='save_db')],
        [InlineKeyboardButton(text=f'Удалить все данные', callback_data='all_del_db')]
    ],
    row_width=1
)
