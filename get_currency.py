import aiohttp
import asyncio


async def execute(from_currency: str, to_currency: str, amount: str) -> str:
    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency}"
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as response:
                data = await response.json()

        if data['result'] == 'error' and data['error-type'] == 'unsupported-code':
            result = (f"Валюта *{from_currency}* не найдена\n"
                      f"Пожалуйста, ознакомьтесь с кодами валют [по ссылке]"
                      f"(https://www.exchangerate-api.com/docs/supported-currencies)")
            return result
        rate = data['rates'][to_currency]
        result = (f"Результат конвертации:\n"
                  f"*{amount} {from_currency} = {float(rate) * float(amount):.2f} {to_currency}*")
    except KeyError:
        result = (f"Валюта *{to_currency}* не найдена\n"
                  f"Пожалуйста, ознакомьтесь с кодами валют [по ссылке]"
                  f"(https://www.exchangerate-api.com/docs/supported-currencies)")
    except ValueError:
        result = (f"Неверный формат суммы {amount}\n"
                  f"Пожалуйста, введите сумму в виде числа"
                  f"(если вы вводите дробное число, пожалуйста, вводите в следующем виде \"0.1\"")

    return result
