from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


format_file_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='XLSX', callback_data='fm_xlsx')],
        [InlineKeyboardButton(text='PDF', callback_data='fm_pdf')],
        [InlineKeyboardButton(text='TIFF', callback_data='fm_tiff')]
    ],
)

