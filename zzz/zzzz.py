import httpx
from loguru import logger

params = {
            'key': '2dbb383a0d8bfd69c22e68f66c3cda80',
            'countries': 'all',
            'types': 'https',
            'level': 'all',
            'speed': '0',
            'count': '0',
        }
with httpx.Client(proxies="http://213.137.240.243:81") as client:
    res = client.get('https://proxoid.net/api/getProxy',params=params, timeout=10)
    pro = [res.text.split("\n")]
    logger.info(f'Прокси получено {len(pro[0])}')
