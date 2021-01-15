import asyncio

from aiogram.utils import executor
from met import Con_DB
from met import Checker
from handlers import dp


async def zzz(wait_for: int, coro):
    while True:
        await asyncio.sleep(wait_for)
        await coro()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(zzz(900, coro=Checker().main))
    executor.start_polling(dp, loop=loop)
