from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

key_check_db = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f'Показать данные в СУБД', callback_data='call_check_db')],
    ],
    row_width=1
)
