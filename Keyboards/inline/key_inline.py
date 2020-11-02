from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def key_inline(message):
    key_inline_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Получить данные по {message}', callback_data='inn')],
            [InlineKeyboardButton(text=f'Добавить к проверке на блок', callback_data='insert')],
            [InlineKeyboardButton(text=f'Удалить из проверки на блок', callback_data='del')]

        ],
        row_width=1
    )
    return key_inline_menu
