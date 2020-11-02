import asyncio

from aiogram.utils import executor

from handlers import dp
from met import async_block

DELAY = 6000000


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, async_block.main, loop)
    executor.start_polling(dp, loop=loop)
