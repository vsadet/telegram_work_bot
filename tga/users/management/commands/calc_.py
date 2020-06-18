import telebot
from tga.settings import TOKEN
bot = telebot.TeleBot(TOKEN)


# первое, второе число и результат калькулятора
res = {"num1": "",
       "do": "",
       "num2": "",
       "result": None
       }


def calc_step_1(message):
    """Ввод первого числа"""
    keyboard = telebot.types.ReplyKeyboardRemove(selective=False) # Удаляем клавиатуру
    msg = bot.send_message(message.chat.id, 'Введи первое число: ', reply_markup=keyboard)
    bot.register_next_step_handler(msg, calc_step_2)


def calc_step_2(message, past_results=None):
    """Обрабатываем введенное число, если не верно, то перезапускаем функцию.
    После просим ввести ДЕЙСТВИЕ с клавиатуры"""
    try:
        if past_results == None:
            int(message.text) + 0
            res["num1"] = message.text
        else:
            res["num1"] = past_results
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True) # формат клавиатуры
        keyboard.row('+', '-', '*', '/')
        msg = bot.send_message(message.chat.id, "Выберите действие: ", reply_markup=keyboard)
        bot.register_next_step_handler(msg, calc_step_3)
    except ValueError:
        msg = bot.send_message(message.chat.id, 'Вы ввели не число, попробуйте еще раз: ')
        bot.register_next_step_handler(msg, calc_step_2)


def calc_step_3(message):
    """Проверяем, что ввели нужный символ или просим ввести заново. После просим ввести 2 число"""
    if message.text == "+" or message.text == "-" or message.text == "*" or message.text == "/":
        res["do"] = message.text
        keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Введи второе число: ', reply_markup=keyboard)
        bot.register_next_step_handler(msg, calc_step_4)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row('+', '-', '*', '/')
        msg = bot.send_message(message.chat.id, "Не верное действие, выберите заново: ", reply_markup=keyboard)
        bot.register_next_step_handler(msg, calc_step_3)


def calc_step_4(message):
    """Проводим вычисления и выясняем желает ли продолжить пользователь вычисления."""
    try:
        int(message.text) + 0
        res["num2"] = message.text
        res["result"] = eval(str(res["num1"]) + res["do"] + str(res["num2"]))
        bot.send_message(message.chat.id, "Результат: " + str(res["result"]))

        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Продолжим', 'С меня хватит!')
        msg = bot.send_message(message.chat.id, "Все клево, продолжать будем? ", reply_markup=keyboard)
        bot.register_next_step_handler(msg, calc_step_5)
    except ValueError:
        msg = bot.send_message(message.chat.id, 'Вы ввели не число, попробуйте еще раз: ')
        bot.register_next_step_handler(msg, calc_step_4)
    except ZeroDivisionError:
        msg = bot.send_message(message.chat.id, 'На ноль делить нельзя, попробуйте еще раз: ')
        bot.register_next_step_handler(msg, calc_step_4)


def calc_step_5(message):
    """Если пользователь желает продолжить вычисления,
    то записываем результат вычислений в значение 1 числа и отправляем на второй шаг"""
    if message.text == 'С меня хватит!':
        bot.send_message(message.chat.id, "Это было здорово, возвращайся")
        # Command.start_message(message)
    elif message.text == 'Продолжим':
        calc_step_2(message, res["result"])
    else:
        msg = bot.send_message(message.chat.id, 'Ввель какую-то ерунду, попробуйте еще раз: ')
        bot.register_next_step_handler(msg, calc_step_5)