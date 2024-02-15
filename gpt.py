import g4f


async def message_answer(message: str) -> str:
    message = [{"role": "user",
                "content": f"Ты бот конвертер валют, ты умеешь конвертировать сумму из одной валюты в другую. "
                           f"Релевантно и лаконично, КАК ЧЕЛОВЕК ответь пользователю на сообщение "
                           f"(максимум 32 слова).\n"
                           f"Пользователь: {message}"}]
    response = await g4f.ChatCompletion.create_async(model="gpt-3.5-turbo",
                                                     messages=message,
                                                     stream=False)

    return response
