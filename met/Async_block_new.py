import asyncio
import os
from asyncio.tasks import shield

import aiosqlite

from data.config import BASE_DIR
from loader import bot
import httpx
from loguru import logger
from fake_useragent import UserAgent


class Blocker:

    def __init__(self, ):
        asyncio.log.logger.setLevel(40)
        self.dir_db = os.path.join(BASE_DIR, 'data', 'test.sql')
        self.__ua = UserAgent().chrome
        self.__base_url = "https://service.nalog.ru/bi2-proc.json"
        self.__headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Host": "service.nalog.ru",
            "Origin": "https://service.nalog.ru",
            "Referer": "https://service.nalog.ru/bi.do",
            "User-Agent": self.__ua
        }
        self.__base_url_proxy = "https://proxoid.net/api/getProxy"
        self.__params = {
            'key': '2dbb383a0d8bfd69c22e68f66c3cda80',
            'countries': 'all',
            'types': 'https',
            'level': 'high, anonymous',
            'speed': '0',
            'count': '0',
        }
        self.__url_check = "https://api.my-ip.io/ip.json"
        self.__good_proxy = []

    @staticmethod
    async def check_block(r):
        data = r.get('datePRS')
        inn = r.get('innPRS')
        if r and 'rows' in r:
            name = r.get('rows')[0].get('NAIM')
            logger.error('БЛОКИРОВКА ' + ' Дата ' + data + ' | ' + name + ' : ' + inn)
            info = f"<b>БЛОКИРОВКА</b>, Дата: {data} | <b>{name}</b> : {inn}"
            await bot.send_message(chat_id=589574396, text=info)
        else:
            logger.success('ВСЕ ХОРОШО ' + ' Дата ' + data + ' | ' + inn)
            info = f"<b>ВСЕ ХОРОШО</b>, Дата: {data} | {inn}"
            # await bot.send_message(chat_id=-1001457324002, text=info)

    async def get_proxy(self):
        pro = []
        logger.info('Запрос прокси')
        async with httpx.AsyncClient() as client:
            response = await client.get(self.__base_url_proxy, params=self.__params)
            pro.append(response.text.split("\n"))
        logger.info(f'Прокси получено {len(pro[0])}')
        return pro[0]

    async def get_ip(self, proxy: str):
        try:
            async with httpx.AsyncClient(proxies=f"http://{proxy}", timeout=10) as client:
                response = await client.get(self.__base_url)
                if response:
                    self.__good_proxy.append(proxy)
        except:
            pass

    async def get_good(self):
        proxies = await shield(self.get_proxy())
        logger.success(f'Проверяем прокси на валидность')
        task = []
        for proxy in proxies:
            task.append(self.get_ip(proxy))
        await asyncio.wait(task)

    async def __rotate_user_agent(self) -> None:
        logger.info('Смена ЮзерАгента')
        self.__ua = UserAgent().chrome

    async def __rotate_proxy(self) -> None:
        self._proxy = self.__good_proxy.pop(-1)

    async def get_info(self, proxy, inn):
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
        while True:
            try:
                await asyncio.sleep(0.1)
                async with httpx.AsyncClient(headers=self.__headers, proxies=f'http://{proxy}', timeout=20) as client:
                    response = await client.get(self.__base_url, params=payload)
                    if response.status_code == 200:
                        r = response.json()
                        await self.check_block(r)
                        break
                    else:
                        await asyncio.sleep(0.1)
                        await self.__rotate_proxy()
                        logger.warning(f'Повторное отправление {inn}  | {self._proxy}')
                        # await self.get_info(proxy=self._proxy, inn=inn)

            except Exception as e:
                await asyncio.sleep(0.1)
                # logger.info(f'Повторное отправление {inn}| {e}')
                await self.__rotate_proxy()

    async def run_all(self):

        logger.info('Проверка на блокировку фирм')
        async with aiosqlite.connect(self.dir_db) as conn:
            cursor = await conn.execute('''SELECT ИНН FROM firms''')
            rows = await cursor.fetchall()
            inn = []
            for row in rows:
                inn.append(row[0])
        logger.info(f'Получено фирм: {len(inn)}')
        await shield(self.get_good())

        logger.success(f'Отобрано {len(self.__good_proxy)} прокси')
        task = []
        for n, i in enumerate(inn):
            task.append(self.get_info(proxy=self.__good_proxy[n], inn=i))
        await asyncio.wait(task)


if __name__ == '__main__':
    c = Blocker()
    asyncio.run(c.run_all())
