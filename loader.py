import logging
# from met.Con_db import Con_DB
from aiogram import Bot, Dispatcher, types

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
dp = Dispatcher(bot)
# db = Con_DB()
