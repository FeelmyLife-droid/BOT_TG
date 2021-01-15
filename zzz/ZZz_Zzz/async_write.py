import datetime
import asyncio
import openpyxl
import pandas as pd
from excel import BASE_DIR

TEMPLATE = openpyxl.load_workbook(f'{BASE_DIR}/data/usn2.xlsx', data_only=True)
SHEET_WB = TEMPLATE['стр.1']


async def check_tel(tel):
    if tel[0] == str(8):
        c = f"+7" + tel[1::]
    else:
        c = tel
    return c


async def get_info(file):
    data = str(datetime.date.today().strftime("%d.%m.%Y"))
    xl = pd.ExcelFile(file)
    sheet = xl.parse('fields')
    sheet2 = xl.parse('ЛистВ_с.1 1')
    info = sheet2[str(sheet2.columns.ravel()[0])].tolist()
    name_ogr = sheet[str(sheet.columns.ravel()[0])].tolist()[0][3::]
    name_dir = info[1]
    fio_dir = info[0]
    last_name_dir = info[2]
    tel_ = await check_tel(info[33])
    return name_ogr, name_dir, fio_dir, last_name_dir, tel_, data


async def write_wb(data, r, s=1):
    global SHEET_WB
    i = 0
    if i != len(data):
        i += 1
        step = int(s)
        for i in data:
            SHEET_WB.cell(row=r, column=step).value = i
            step += 3


async def main(file):
    global TEMPLATE
    info = await get_info(file)
    await write_wb(info[0], 17)
    await write_wb(info[1], 45)
    await write_wb(info[2], 43)
    await write_wb(info[3], 47)
    await write_wb(info[4], 53)
    await write_wb(info[5], 57, s=31)
    file_name = f'{info[0][2:-1]} Заявление на применение Упрощеного режима.xlsx'
    TEMPLATE.save(f'{BASE_DIR}/excel/{info[0][2:-1]} Заявление на применение Упрощеного режима.xlsx')
    return file_name



