from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

key_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Новые адреса'),
            KeyboardButton(text='Блокировка Фирм')
        ],
        [
            KeyboardButton(text='Данные по ИНН'),
            KeyboardButton(text='Выписка из ЕГРЛ')
        ]
    ],
    resize_keyboard=True)
