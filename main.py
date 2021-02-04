import asyncio

from aiogram.utils import executor

from handlers import dp


async def zzz(wait_for: int, coro):
    while True:
        await asyncio.sleep(wait_for)
        await coro()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    executor.start_polling(dp, loop=loop)
