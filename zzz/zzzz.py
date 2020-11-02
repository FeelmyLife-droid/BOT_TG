import asyncio
import logging
import os

import aiosqlite as aiosqlite
import httpx
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from fake_useragent import UserAgent

from met import async_block, async_rus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
bot = Bot(token='1201963552:AAFKHdlv-phjJA64MH1C3NCKYrMBXtcmJDs', parse_mode='HTML')
dp = Dispatcher(bot)
DELAY = 60


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first_btn = types.KeyboardButton(text='Новые адреса')
    second_btn = types.KeyboardButton(text='Блокировка Фирм')
    third_btn = types.KeyboardButton(text='Данные по ИНН')
    fourth_btn = types.KeyboardButton(text='Выписка из ЕГРЛ')
    keyboard_markup.add(first_btn, second_btn, third_btn, fourth_btn)
    await message.answer(f"Привет <b>{message.chat.first_name}</b>!\nНачнем?", reply_markup=keyboard_markup)


@dp.callback_query_handler()
async def call_inn(call: types.CallbackQuery):
    keymap = types.InlineKeyboardMarkup(row_width=1)
    btn_add = types.InlineKeyboardButton(text="Добавить в базу данных", callback_data='add')
    keymap.add(btn_add)

    if call.data == 'inn':
        print(call)
        ua = UserAgent().chrome
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'www.rusprofile.ru',
            'Referer': 'https://www.rusprofile.ru/',
            'TE': 'Trailers',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua
        }
        async with httpx.AsyncClient(headers=headers) as client:
            r = await client.get(
                f"https://www.rusprofile.ru/ajax.php?=&query={call.message.reply_to_message.text}&action=search")
        res = r.json()
        name_org = res['ul'][0]['name']
        ogrn_org = res['ul'][0]['ogrn']
        inn_org = str(res['ul'][0]['inn'])[3:13]
        region_org = res['ul'][0]['region']
        address_org = res['ul'][0]['address']
        position = res['ul'][0]['ceo_type']
        position_fio = res['ul'][0]['snippet_string']
        okved_org = res['ul'][0]['main_okved_id']
        okved_descr = res['ul'][0]['okved_descr']
        capital = str(res['ul'][0]['authorized_capital']).split(".")[0]
        date_reg_org = res['ul'][0]['reg_date']
        reply_text = (f'НАЗВАНИЕ :<b>{name_org}</b>/\n'
                      f'ОГРН : <b>{ogrn_org}</b>/\n'
                      f'ИНН : <b>{inn_org}</b>\n'
                      f'РЕГИОН : <b>{region_org}</b>\n'
                      f'АДРЕСС : <b>{address_org}</b>\n'
                      f'{position} : <b>{position_fio}</b>\n'
                      f'{okved_org} : <b>{okved_descr}</b>\n'
                      f'УСТАВНОЙ КАПИТАЛ : <b>{capital}</b>\n'
                      f'ДАТА РЕГ : <b>{date_reg_org}</b>')
        await call.message.answer(reply_text, reply_markup=keymap)

    if call.data == 'insert':
        async with aiosqlite.connect('test.sql') as db:
            async with db.execute(f'''SELECT * FROM test WHERE ИНН={call.message.reply_to_message.text} ''') as cur:
                firm = await cur.fetchone()
                if firm:
                    await call.message.answer(f'{firm[0][:-1:]} уже есть в списке на проверку')
                else:
                    await call.message.answer(f'такого {call.message.reply_to_message.text} нет')

        await cur.close()
        await db.close()

    if call.data == 'add':  # Ошибка 'ValueError: no active connection' надо исправить
        info = []
        i = call.message.text.split('\n')
        for n in i:
            k = n.split(":")
            info.append(str(k[1]))
        async with aiosqlite.connect('test.sql') as db:
            cursor = await db.execute('''CREATE TABLE IF NOT EXISTS test(
                Название TEXT NOT NULL,
                ОГРН INTEGER NOT NULL,
                ИНН INTEGER NOT NULL,
                Регион TEXT,
                Адресс TEXT,
                Директор TEXT,
                ОКВЭД TEXT,
                Уставной капилал INTEGER NOT NULL,
                Дата_рег TEXT)''')
            await cursor.close()
            await db.close()
        await asyncio.sleep(2)
        async with aiosqlite.connect('test.sql') as conn:
            await conn.execute(f'''INSERT INTO test VALUES (?,?,?,?,?,?,?,?,?);''', info)
            await conn.commit()
            await conn.close()


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    button_text = message.text
    logger.debug('The answer is %r', button_text)
    if button_text == 'Новые адреса':
        file_path = str(async_rus.get_date()[1] + ' ' + async_rus.get_date()[0]) + '.xlsx'
        if os.path.exists(file_path):
            reply_text = f"Фирм зарегистрированные за {file_path.split('.')[0]}"  # добавить скрипт отправки файла
            doc = open(f'{file_path}', 'rb')
            await bot.send_document(message.chat.id, doc)
            await message.answer(reply_text)
        else:
            reply_text = f"Фирмы зарегистрированные за {file_path.split('.')[0]}"
            await async_rus.main()
            doc = open(f'{file_path}', 'rb')
            await bot.send_document(message.chat.id, doc)
            await message.answer(reply_text)
    if message.text.isdigit() and len(message.text) == 10:
        inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text=f'Получить данные по {message.text}', callback_data='inn')
        btn2 = types.InlineKeyboardButton(text=f'Добавить к проверке на блок', callback_data='insert')
        btn3 = types.InlineKeyboardButton(text=f'Удалить из проверки на блок', callback_data='del')
        inline_keyboard.add(btn1, btn2, btn3)
        await message.reply(text='Выберите действие', reply_markup=inline_keyboard)


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, async_block.main, loop)
    executor.start_polling(dp, loop=loop)
