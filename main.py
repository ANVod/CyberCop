import telebot
from datetime import datetime

# Токен API к Telegram боту - замените 'YOUR_BOT_TOKEN' на ваш токен
TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

# Функция приветствия
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я простой эхо-бот. Отправь мне что-нибудь, и я отправлю это обратно!")

# Функция вывода текущей даты и времени
@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.reply_to(message, f"Текущее время: {current_time}")

# Эхо-функция: повторяет полученные сообщения
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск бота
bot.polling()