from aiogram import types

from Keyboards.inline.inline_insert_db import key_insert_db
from loader import dp
from met.get_name_org import get_name_firm


@dp.callback_query_handler(text='inn')
async def call_inn(call: types.CallbackQuery):
    c = await get_name_firm(call.message.reply_to_message.text)
    reply_text = (f'НАЗВАНИЕ :<b>{c.get("name_org")}</b>\n'
                  f'ОГРН : <b>{c.get("ogrn_org")}</b>\n'
                  f'ИНН : <b>{c.get("inn_org")}</b>\n'
                  f'РЕГИОН : <b>{c.get("region_org")}</b>\n'
                  f'АДРЕСС : <b>{c.get("address_org")}</b>\n'
                  f'{c.get("position")} : <b>{c.get("position_fio")}</b>\n'
                  f'{c.get("okved_descr")} : <b>{c.get("capital")}</b>\n'
                  f'УСТАВНОЙ КАПИТАЛ : <b>{c.get("date_reg_org")}</b>\n'
                  f'ДАТА РЕГ : <b>{c.get("okved_org")}</b>')
    await call.message.answer(reply_text, reply_markup=key_insert_db)
