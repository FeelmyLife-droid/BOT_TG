import os
import random

from data.config import BASE_DIR
from loader import bot
import asyncio
from asyncio.tasks import shield
import aiosqlite
import httpx
from loguru import logger
from fake_useragent import UserAgent


class Checker:

    def __init__(self, ):
        asyncio.log.logger.setLevel(40)
        self.dir_db = os.path.join(BASE_DIR, 'data', 'test.sql')
        self.__ua = UserAgent().chrome
        self.__url_token = "https://pb.nalog.ru/search-proc.json"
        self.__headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "DNT": "1",
            "Host": "pb.nalog.ru",
            "Origin": "https://pb.nalog.ru",
            "Referer": "https://pb.nalog.ru/search.html",
            "User-Agent": self.__ua
        }
        self.__url_proxy = "https://proxoid.net/api/getProxy"
        self.__params = {
            'key': '2dbb383a0d8bfd69c22e68f66c3cda80',
            'countries': 'all',
            'types': 'https',
            'level': 'high,anonymous',
            'speed': '0',
            'count': '0',
        }
        self.__url_check = "https://pb.nalog.ru/company-proc.json"
        self.__good_proxy = []
        self.__token = []
        self._proxy = ""

    async def fetch_token(self, r: dict):
        """OK"""
        data = r.get('ul').get('data')[0]
        token = data.get('token')

        self.__token.append(token)

    async def get_proxy(self):
        """Получение прокси возращает список всххех прокси"""
        pro = []
        logger.info('Запрос прокси')
        async with httpx.AsyncClient() as client:
            response = await client.get(self.__url_proxy, params=self.__params)
            pro.append(response.text.split("\n"))
        logger.info(f'Прокси получено {len(pro[0])}')
        return pro[0]

    async def get_ip(self, proxy: str):
        try:
            async with httpx.AsyncClient(proxies=f"http://{proxy}", timeout=10) as client:
                response = await client.get(self.__url_token, )
                res = response.json()
                if response:
                    self.__good_proxy.append(proxy)
        except:
            pass

    async def get_good(self):
        """Проверка прокси на валидность для сайта налоговой"""
        proxies = await self.get_proxy()
        logger.success(f'Проверяем прокси на валидность')
        task2 = []
        for proxy in proxies:
            task2.append(self.get_ip(proxy))
        await asyncio.wait(task2)

    async def __rotate_user_agent(self) -> None:
        """Смена юзер Агента"""
        self.__ua = UserAgent().chrome

    async def __rotate_proxy(self) -> None:
        """Смена прокси"""
        self._proxy = random.choice(self.__good_proxy)

    async def get_token(self, inn):
        """ Получение токенов с сайта  налоговой для дальнейшей отправки"""
        if len(str(inn)) == 10:
            # await self.__rotate_proxy()
            # await self.__rotate_user_agent()
            params = {
                "page": "1",
                "pageSize": "10",
                "pbCaptchaToken": "",
                "token": "",
                "mode": "search-all",
                "queryAll": str(inn),
                "queryUl": "",
                "okvedUl": "",
                "statusUl": "",
                "regionUl": "",
                "isMspUl": "",
                "mspUl1": "1",
                "mspUl2": "2",
                "mspUl3": "3",
                "queryIp": "",
                "okvedIp": "",
                "statusIp": "",
                "regionIp": "",
                "isMspIp": "",
                "mspIp1": "1",
                "mspIp2": "2",
                "mspIp3": "3",
                "queryUpr": "",
                "uprType1": "1",
                "uprType0": "1",
                "queryRdl": "",
                "dateRdl": "",
                "queryAddr": "",
                "regionAddr": "",
                "queryOgr": "",
                "ogrFl": "1",
                "ogrUl": "1",
                "npTypeDoc": "1",
                "ogrnUlDoc": "",
                "ogrnIpDoc": "",
                "nameUlDoc": "",
                "nameIpDoc": "",
                "formUlDoc": "",
                "formIpDoc": "",
                "ifnsDoc": "",
                "dateFromDoc": "",
                "dateToDoc": ""
            }
            while True:
                await asyncio.sleep(0.1)
                await self.__rotate_proxy()
                await self.__rotate_user_agent()
                try:
                    await asyncio.sleep(0.1)
                    async with httpx.AsyncClient(headers=self.__headers, proxies=f'http://{self._proxy}') as client:
                        response = await client.post(self.__url_token, params=params)
                        if response.status_code == 200:
                            r = response.json()

                            await self.fetch_token(r)
                            break
                        else:
                            await self.__rotate_user_agent()
                            await self.__rotate_proxy()
                            await self.get_token(inn=inn)

                except Exception as e:
                    await asyncio.sleep(0.1)
                    await self.__rotate_user_agent()
                    await self.__rotate_proxy()
                    logger.warning(f'ОШИБКА| {e} | {self._proxy} | {inn}')

    @staticmethod
    async def check_changes(res: dict):
        """Вывод информации о статусе фирмы"""

        data = res.get('vyp')
        name_firm = data.get('НаимЮЛПолн')
        print(name_firm)
        inn = data.get('ИНН')
        if 'СвНедАдресЮЛ' in data:
            info = data.get('СвНедАдресЮЛ')[0]
            mes = f'Название:{name_firm}\nИНН:{inn}\n\tТекст:<b>СВЕДЕНИЯ О НЕДОСТОВЕРНОСТИ ДАННЫХ ОБ АДРЕСЕ </b>'
            # print(mes)
            # await shield(bot.send_message(chat_id=589574396, text=mes))
            await shield(bot.send_message(chat_id=-1001457324002, text=mes))
        elif 'СведДолжнФЛ' in data:
            info = data.get('СведДолжнФЛ')[0]
            sugn = info.get('СвНедДанДолжнФЛ')[0]
            mes = f'Название:{name_firm}\nИНН:{inn}\n\tТекст:<b>СВЕДЕНИЯ О НЕДОСТОВЕРНОСТИ ДАННЫХ О РУКОВОДИТЕЛЕ ' \
                  f'КОМПАНИИ</b>\n\t{sugn.get("ТекстНедДанДолжнФЛ")}\n\tДата записи:{sugn.get("ДатаЗаписи")}'
            # print(mes)
            # await shield(bot.send_message(chat_id=589574396, text=mes))
            await shield(bot.send_message(chat_id=-1001457324002, text=mes))

    async def data_for_token(self, token):
        # await self.__rotate_proxy()
        # await self.__rotate_user_agent()
        params2 = {'token': str(token)}

        while True:
            await self.__rotate_proxy()
            await self.__rotate_user_agent()
            try:
                await asyncio.sleep(0.1)
                async with httpx.AsyncClient(proxies=f'http://{self._proxy}', timeout=10) as client:
                    response = await client.post(self.__url_check, params=params2)
                    if response.status_code == 200:
                        e = response.json()
                        # print(e)
                        await self.check_changes(e)
                        break
                    else:
                        await asyncio.sleep(0.1)
                        await self.__rotate_proxy()
                        logger.warning(f'Повторное отправление {token}')
                        await self.data_for_token(token=token)
            except Exception as e:
                await asyncio.sleep(0.1)
                logger.error(f'Повторное отправление |{token}|{e}')
                await self.__rotate_proxy()

    async def run_all(self):
        async with aiosqlite.connect(self.dir_db) as conn:
            cursor = await conn.execute('''SELECT ИНН FROM firms''')
            rows = await cursor.fetchall()
            inn = []
            for row in rows:
                inn.append(row[0])
        await shield(self.get_good())
        logger.success(f'Отобрано {len(self.__good_proxy)} прокси')
        logger.info(f'{len(inn)}')
        task1 = []
        for i in inn:
            task1.append(self.get_token(inn=i))
        await asyncio.wait(task1)

    async def main(self):
        logger.info('Проверка на изменения')
        await shield(self.run_all())
        logger.success(f'Получено {len(self.__token)} токенов')
        task = []
        for i in self.__token:
            task.append(self.data_for_token(token=i))
        await shield(asyncio.wait(task))
        self.__good_proxy.clear()
        self.__token.clear()


if __name__ == '__main__':
    c = Checker()
    asyncio.run(c.main())
