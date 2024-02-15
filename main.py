import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram import filters

from loguru import logger

import dotenv
import os

import gpt
import get_currency

dotenv.load_dotenv()

dp = Dispatcher()


@dp.message(filters.Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я готов помочь с конвертацией валют. Чем могу помочь?")


@dp.message(filters.Command("help"))
async def send_help(message: types.Message):
    await message.reply(
        "Чтобы произвести конвертацию валюты, введите команду `/convert`, укажите сумму и валюты.\n\n"
        "*Например*: `/convert 100 usd to rub`",
        parse_mode="Markdown"
    )


@dp.message(filters.Command("convert"))
async def convert_currency(message: types.Message):
    text = message.text.split(" ")
    amount = text[1]
    from_currency = text[2].upper()
    to_currency = text[4].upper()

    result = get_currency.get_currency(from_currency, to_currency, amount)

    await message.reply(result, parse_mode="Markdown", disable_web_page_preview=True)


@dp.message()
async def get_message(message: types.Message):
    gpt_answer = await gpt.message_answer(message.text)
    await message.reply(gpt_answer)


async def main() -> None:
    api_token = os.getenv('API_TOKEN')
    bot = Bot(token=api_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
