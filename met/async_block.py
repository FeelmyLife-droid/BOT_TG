import asyncio
from asyncio.tasks import shield

import httpx
from fake_useragent import UserAgent
from loguru import logger

import main


async def get_good():
    global good
    proxies = await get_proxy()
    task = []
    for i in proxies:
        task.append(get_ip(i))
    await asyncio.wait(task)


async def get_ip(proxy):
    global good_pro
    try:
        url = 'https://api.my-ip.io/ip.json'
        async with httpx.AsyncClient(proxies=f"http://{proxy}", verify=False, timeout=10) as client:
            response = await client.get(url)
            r = response.json()
        good_pro.append(proxy)
        logger.success(f'{proxy} Сработал')
    except Exception as e:
        pass


async def get_proxy():
    logger.info('Получаем прокси с сайта')
    proxies = []
    url = 'https://proxoid.net/api/getProxy'
    params = {
        'key': 'c5d6be15ad7fbc8508736c7268b1152a',
        'countries': 'all',
        'types': 'https',
        'level': 'high,anonymous',
        'speed': '800',
        'count': '0',
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    proxies.append(response.text.split('\n'))
    logger.info('Прокси получены')
    logger.success('Записываем в словарь')
    print(len(proxies[0]))
    return proxies[0]


async def get_info(inn, proxy):
    replay = []
    try:
        """Получение данных с сайта налоговой"""
        ua = UserAgent().random
        URL = "https://service.nalog.ru/bi2-proc.json"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Host": "service.nalog.ru",
            "Origin": "https://service.nalog.ru",
            "Referer": "https://service.nalog.ru/bi.do",
            "User-Agent": ua
        }
        payload = {
            "requestType": "FINDPRS",
            "innPRS": str(inn),
            "bikPRS": "044525225",
            "fileName": "",
            "bik": "",
            "kodTU": "",
            "dateSAFN": "",
            "bikAFN": "",
            "dateAFN": "",
            "fileNameED": "",
            "captcha": "",
            "captchaToken": ""
        }
        logger.info('Отправляем запрос по ' + str(inn))
        async with httpx.AsyncClient(headers=headers, proxies=f"http://{proxy}", timeout=30) as client:
            response = await client.get(URL, params=payload)
            r = response.json()
        await check_block(r)
    except Exception as e:
        logger.warning(f'{inn} не прошел проверку по причине {e}')


async def check_block(r):
    global info
    try:
        if r:
            if 'rows' in r:
                data = r.get('datePRS')
                inn = r.get('innPRS')
                name = r.get('rows')[0].get('NAIM')
                logger.error('БЛОКИРОВКА ' + ' Дата ' + data + ' | ' + name + ' : ' + inn)
                reply_text = f"'БЛОКИРОВКА ' + ' Дата ' + {data} + ' | ' + {name} + ' : ' + {inn})"
                await main.bot.send_message(reply_text)
            else:
                data = r.get('datePRS')
                inn = r.get('innPRS')
                logger.success('ВСЕ ХОРОШО ' + ' Дата ' + data + ' | ' + inn)
                reply_text = f"'ВСЕ ХОРОШО ' + ' Дата ' + {data} + ' | ' + {inn})"
                await main.bot.send_message(reply_text)
                # info = 'ВСЕ ХОРОШО ' + ' Дата ' + data + ' | ' + inn
    except Exception as e:
        logger.warning(f'Some shit happens: ' + str(e) + r)


async def main():
    global good_pro
    good_pro = []
    await shield(get_good())
    task1 = []
    inn = [2461043779, 7727397714, 9719003695, 6166119523, 6166119347, 6166110898, 6166110880, 6166111475,
           2311293603, 2311286081, 6452137386]
    for n, i in enumerate(inn):
        task1.append(get_info(i, good_pro[n]))
    await asyncio.wait(task1)
    await asyncio.sleep(60)


if __name__ == '__main__':
    while True:
        asyncio.run(main())
