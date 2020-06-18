from django.core.management.base import BaseCommand
import telebot

from users.management.commands.calc_ import calc_step_1
from tga.settings import TOKEN
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Обработка start"""
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Привет', 'Пока', 'Калькулятор')
    # Users(message.from_user.id, message.from_user.first_name, message.chat.id)
    bot.send_message(message.chat.id, f'{message.chat.first_name}, чем займемся?', reply_markup=keyboard)
    print(message.text)


@bot.message_handler(content_types=['text'])
def send_text(message):
    """Обработка выбранного варианта"""
    if message.text == 'Привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text == 'Калькулятор':
        calc_step_1(message)
    else:
        print("else", message.text)
        start_message()

bot.polling()
