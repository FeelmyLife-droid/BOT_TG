from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

key_insert_db = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Добавить в базу данных', callback_data='insert')],
        ],
        row_width=1
    )

