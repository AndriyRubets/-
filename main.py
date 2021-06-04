import requests
import datetime
from auth_data import weather_token, bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# всі необхідні бібліотеки

bot = Bot(token=bot_token) #створюю об'єкт бота
dp = Dispatcher(bot) #створюю змінну та вписую в неї об'єкт диспетчер в який приймає значення bot

@dp.message_handler(commands=["start"]) #створюю декоратор функції, та вказую на яку команду бот має відкликатись
async def start_command(message: types.Message): #створюю функцію для написання відповіді ботом на команду
    await message.reply("Hello user! You can use this command: /weather and mooooooore")# бот відповідає

@dp.message_handler(commands=["weather"])#створюю декоратор функції, та вказую на яку команду бот має відкликатись
async def start_command(message: types.Message):#створюю функцію для написання відповіді ботом на команду
    await message.reply("Enter name of the city, if you want to know weather forecast:") # бот відповідає


@dp.message_handler()
async def get_weather(message: types.Message): #створюю функцію для виводу погоди
    code_to_smile = { #в даному блоці присвоюю певній погоді своє емодзі
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Drizzle \U00002614",
        "Thunderstorm": "Thunder \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }

    try:
        r = requests.get( #створюю зміннту по якій зроблю запит та отримаю дані
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric"
        )
        data = r.json()# робимо get запит на API та отримуємо дані з JSON

        city = data["name"] #витягую з json тільки потрібні значення
        cur_weather = data["main"]["temp"]# поточна погода

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile: # В даній умові,якщо по запиту прийде невідома погода, яку я не використовую з вищеперечислених, тоді бот дасть повідомлення про помилку і код не піде далі
            wd = code_to_smile[weather_description]
        else:
            wd = "I dont know this kind of weather "

        humidity = data["main"]["humidity"] #вологість
        pressure = data["main"]["pressure"] #тиск
        wind = data["wind"]["speed"] #швидкість вітру
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])# схід сонця
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) #захід сонця
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"]) # вказується поточна довжина дня від сходу сонця до заходу сонця

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n" #роблю вивід в стовпчик повідомлень, що будуть приймати значення 
              f"City weather: {city}\nTemperature: {cur_weather}C° {wd}\n"
              f"Humidity: {humidity}%\nPressure: {pressure} mm. mm.\nWind: {wind} m/s\n"
              f"Sunrice: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nLength of the day: {length_of_the_day}\n"
              f"***Have a nice day!***"
              )

    except: # в блоці except роблю вивід про помилку
        await message.reply("\U00002620 Oh no! I guess you write wrong city name. Please try again \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp) #через if-main викликаю з aiogram executor в якого викликається метод start_polling(dp) для запуску бота
