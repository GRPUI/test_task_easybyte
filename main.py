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
api_token = os.getenv('API_TOKEN')
bot = Bot(token=api_token)

CURRENCY_CODES_INLINE_KEYBOARD = types.InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text='Коды поддерживаемых валют',
                web_app=types.WebAppInfo(
                    url=f'https://www.exchangerate-api.com/docs/supported-currencies'
                )
            )
        ]
    ]
)


@dp.message(filters.Command("start"))
async def send_welcome(message: types.Message):
    logger.info(f"User:{message.from_user.id} Command: /start")
    await logger.complete()
    await bot.set_chat_menu_button(
        message.chat.id,
        types.MenuButtonWebApp(
            text="Коды валют",
            web_app=types.WebAppInfo(url="https://www.exchangerate-api.com/docs/supported-currencies")
        )
    )
    await message.reply("Привет! Я готов помочь с конвертацией валют. Чем могу помочь?")


@dp.message(filters.Command("help"))
async def send_help(message: types.Message):
    logger.info(f"User:{message.from_user.id} Command: /help")
    await logger.complete()
    await message.reply(
        "Чтобы произвести конвертацию валюты, введите команду `/convert`, укажите сумму и валюты.\n\n"
        "*Например*: `/convert 100 usd to rub`\n"
        "Также вы можете узнать коды поддерживаемых валют, нажав на кнопку ниже",
        parse_mode="Markdown",
        reply_markup=CURRENCY_CODES_INLINE_KEYBOARD
    )


@dp.message(filters.Command("convert"))
async def convert_currency(message: types.Message):
    text = message.text.split(" ")

    if len(text) != 5:
        await message.reply("Неверный ввод. Пожалуйста введите в следующем формате:\n"
                            "`/convert 100 usd to rub`", parse_mode="Markdown")
        logger.info(f"User: {message.from_user.id} Text: {message.text} Error: wrong format")
        await logger.complete()
        return

    amount = text[1]
    from_currency = text[2].upper()
    to_currency = text[4].upper()

    logger.info(f"User:{message.from_user.id} Command: /convert "
                f"Amount: {amount} From_Currency: {from_currency} To_Currency: {to_currency}")

    result = await get_currency.execute(from_currency, to_currency, amount)

    logger.info(f"User:{message.from_user.id} Result: {result}")

    await logger.complete()
    await message.reply(result, parse_mode="Markdown", disable_web_page_preview=True)


@dp.message()
async def get_message(message: types.Message):
    gpt_answer = await gpt.message_answer(message.text)

    logger.info(f"User:{message.from_user.id} Message: {message.text} GPT-3.5-Turbo: {gpt_answer}")

    await logger.complete()
    await message.reply(gpt_answer)


async def main() -> None:
    logger.info("Starting bot")
    await logger.complete()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.add("logs.log", level="INFO", rotation="1 week")
    asyncio.run(main())
