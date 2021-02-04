import asyncio
import locale
import os
from asyncio import shield
from datetime import datetime
from data.config import BASE_DIR
import pandas as pd
import pymorphy2
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader
from met import convert_docx_to_pdf


async def get_image(img: str):
    wb = load_workbook(os.path.join(BASE_DIR, 'excel', 'Регистрация.xlsx'))
    sheet = wb['Регистрация']
    image_loader = SheetImageLoader(sheet)
    image = image_loader.get(img)
    image.save(os.path.join(BASE_DIR, 'excel', f'{img}.png'))


async def get_info(x: dict, image: str):
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    doc = DocxTemplate(os.path.join(BASE_DIR, 'data', 'Reshenie_edinstvennogo_uchreditelja.docx'))
    morph = pymorphy2.MorphAnalyzer()
    e = ''
    for word in x.get('ФИО').split(" "):
        e += str("".join(morph.parse(word)[0].inflect({'gent'}).word.title()) + " ")
    context = {
        "Image": InlineImage(doc, os.path.join(BASE_DIR, 'excel', f"V{2 + int(image)}.png"), width=Mm(40)),
        "НАЗВАНИЕ": x.get("Фирма").strip(),
        "ЮР_ГОР": x.get("Юр. Адрес"),
        "ДАТА": datetime.today().strftime("%d %B %Y года."),
        "ФИО": x.get("ФИО"),
        "НОМЕР_УСТАВА": x.get("НОМЕР.УСТАВА"),
        "ИНН": x.get("ИНН"),
        "СУММ_ПРО": x.get("Уст.Кап")
    }

    doc.render(context)
    doc.save(os.path.join(BASE_DIR, 'excel', f'{x.get("Фирма").strip()}.docx'))
    return f'{x.get("Фирма").strip()}.docx'


async def get_image_xlsx():
    print('Получаем фото подписи')
    excel = pd.read_excel(os.path.join(BASE_DIR, 'excel', 'Регистрация.xlsx'), sheet_name='Регистрация').to_dict(
        'index')
    for i in range(len(excel)):
        await shield(get_image(f'V{2 + int(i)}'))
    print('Подписи получены')


async def write_docx():
    print('Записываем данные')
    await asyncio.sleep(3)
    excel = pd.read_excel(os.path.join(BASE_DIR, 'excel', 'Регистрация.xlsx'), sheet_name='Регистрация').to_dict(
        'index')
    for i in range(len(excel)):
        file = await get_info(excel[i], image=str(i))
        print(file)
        await convert_docx_to_pdf.to_tiff(file)


async def main():
    await asyncio.gather(
        asyncio.create_task(get_image_xlsx()),
        asyncio.create_task(write_docx()),
    )


if __name__ == '__main__':
    asyncio.run(main())
