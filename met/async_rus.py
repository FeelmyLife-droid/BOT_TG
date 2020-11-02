import asyncio
import httpx
import pandas
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger

name_org, adress, inn_org, ogrn_org, kapital, data_reg, okved_org = [], [], [], [], [], [], []


def get_date():
    """Получение даты для автоматической работы"""
    today = datetime.today()
    date = today - timedelta(days=1)
    yesterday = date.strftime("%Y-%m-%d")
    month = today.strftime("%b")
    return yesterday, month


async def get_count(url):
    ua = UserAgent().chrome
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': '???',
        'DNT': '1',
        'Host': 'www.rusprofile.ru',
        'Referer': 'https://www.rusprofile.ru/codes/90000',
        'TE': 'Trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua
    }
    response = httpx.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    count = soup.find('ul', class_='paging-list').find_all('a')[-2].text
    return count


async def fetch(url):
    """Получение страницы HTML"""
    logger.info(f'Получаем данные с {url}')
    ua = UserAgent().chrome
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Connection': 'keep-alive',
        'Cookie': '???',
        'DNT': '1',
        'Host': 'www.rusprofile.ru',
        'Referer': 'https://www.rusprofile.ru/codes/90000',
        'TE': 'Trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        await get_data(response.text)


async def get_data(data):
    """Получение данных со страницы"""
    global link, name, org, adr
    info_company = []
    soup = BeautifulSoup(data, 'lxml')
    all_company = soup.find_all('div', class_='company-item')
    for company in all_company:
        links = company.find_all('a')
        for url in links:  # Название и ссылка ОК
            link = url.get('href')
            name = url.text.strip()
        address = company.find_all('address', class_='company-item__text')
        for a in address:  # Адресс компании ОК
            adr = a.text.strip()
        info = company.find_all('dl')
        dict_info = {}
        for i in info:
            tag = i.find('dt').text
            values = i.find('dd').text
            z = {tag: values}

            dict_info.update(z)
            org = {  # Пополняй словарь
                "name": name,
                "url": "https://www.rusprofile.ru" + link,
                "address": adr,
                "info": dict_info
            }
        info_company.append(org)
    await get_info(info_company)


async def get_info(data):
    """Создание словарей для записи """
    global name_org, adress, inn_org, ogrn_org, kapital, data_reg, okved_org
    if data:
        for o in data:
            name_org.append(o.get('name'))
            adress.append(o.get('address'))
            inn_org.append(o['info'].get('ИНН'))
            ogrn_org.append(o['info'].get('ОГРН'))
            kapital.append(o['info'].get('Уставный капитал'))
            data_reg.append(o['info'].get('Дата регистрации'))
            okved_org.append(o['info'].get('Основной вид деятельности'))
    await write_exl(name_org=name_org, adress=adress, inn_org=inn_org, ogrn_org=ogrn_org, data_reg=data_reg,
                    okved_org=okved_org, kapital=kapital)


async def write_exl(name_org, adress, inn_org, ogrn_org, kapital, data_reg, okved_org):
    """Запись в ексель файл"""
    logger.info('Запись данныхв файл')
    file = str(get_date()[1] + ' ' + get_date()[0])
    df = pandas.DataFrame()
    df['Название'] = name_org
    df['Адрес'] = adress
    df['ИНН'] = inn_org
    df['ОГРН'] = ogrn_org
    df['Уставный капитал'] = kapital
    df['Дата_рег'] = data_reg
    df['ОКВЕД'] = okved_org

    writer = pandas.ExcelWriter(f'./excel/{file}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Лист1', index=False)

    writer.sheets['Лист1'].set_column('A:A', 30)
    writer.sheets['Лист1'].set_column('B:B', 100)
    writer.sheets['Лист1'].set_column('C:C', 12)
    writer.sheets['Лист1'].set_column('D:D', 15)
    writer.sheets['Лист1'].set_column('E:E', 12)
    writer.sheets['Лист1'].set_column('F:F', 15)
    writer.sheets['Лист1'].set_column('G:G', 100)
    logger.info('Сохраняем данные в файл')
    writer.save()


async def scrape_task(url):
    html = await fetch(url)
    # await write_exl(name_org=name_org, adress=adress, inn_org=inn_org, ogrn_org=ogrn_org, data_reg=data_reg,
    #                 okved_org=okved_org, kapital=kapital)


async def main():
    global name_org, adress, inn_org, ogrn_org, kapital, data_reg, okved_org
    url = 'https://www.rusprofile.ru/date/' + get_date()[0]
    logger.info('Начинаем сбор данных')
    count = await get_count(url)
    logger.info(f'Найдено {count} страниц')
    tasks = []
    for i in range(1, int(count) + 1):
        tasks.append(scrape_task(url + '/' + str(i)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
