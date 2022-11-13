
'''
	November Tracker
'''
#5664434829:AAGUxbYiNoKCqXSJwm62IS-vq2tVKjcWjD4
#	Imports
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio
import datetime
import time
import os


#	Settings
api_token = "TOKEN_BOT" # АПИ Твоего Бота
bot = Bot(token=api_token)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop() # Включаем LOOP
delay = 60*3 # Интервал по отправке картинок(в сек.)
count_photo = 1 # Самое первое название картинки

#	Function
def get_datatime(type_datetime = "dt"):

	if type_datetime == "dt":
		get_moment = datetime.datetime.now()
		moment = str(get_moment)

	return moment


#	AIOGRAM

# При старте
@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message):

	btn_exit = KeyboardButton('Сдаюсь!')# Создаём кнопки быстрого доступа
	# Постим кнопки
	main_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(btn_exit)

	print("Отправляю приветствие") # Для отчётности нам в терминал

	# Отправляем ГС с интересным приветствием
	await bot.send_voice(message.from_user.id, 
		open('hallo.wav', 'rb'), 
		reply_markup = main_menu)
	# С помощью асинхронности отправляем поток в 
	asyncio.ensure_future(send_photo(message))

#	При команде Здаюсь
@dp.message_handler(content_types="text")
async def command_help(message: Message):
	if message.text == "Сдаюсь!":
		await bot.send_voice(message.from_user.id, open('bye.wav', 'rb'))


async def send_photo(message):
	global count_photo
	# Проверка на существование файла
	print("Отправляю файл")
	await bot.send_photo(chat_id=message.from_user.id, photo=open(str(count_photo) + ".jpg", 'rb'))
	count_photo += 1

	await asyncio.sleep(delay)

	asyncio.ensure_future(my_callback(message))

def my_callback(message):
	asyncio.ensure_future(send_photo(message))


# RUN
async def main():
	await dp.start_polling(bot)
	loop.run_forever()

if __name__ == "__main__":
    asyncio.run(main())