import telebot
from random import randint

bot = telebot.TeleBot('8181700980:AAFw-EsOg3F0CUdkyVETdLS5LqKMQbTOvew')

users = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = telebot.types.InlineKeyboardButton(
        text="Начать игру", )
    keyboard.add(button_start)
    bot.send_message(message.chat.id,
                     'Добро пожаловать в игру "Угадай число!"',
                     reply_markup=keyboard)


@bot.message_handler(
    func=lambda message: message.text == 'Начать игру')
def start_new_game(message):
    users[message.chat.id] = {}
    users[message.chat.id]['min'] = 1
    users[message.chat.id]['max'] = 100
    bot.register_next_step_handler(message, get_answer)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_ready = telebot.types.InlineKeyboardButton(
        text="Загадал", )
    keyboard.add(button_ready)
    bot.send_message(message.chat.id,
                     'Загадайте число от 1 до 100',
                     reply_markup=keyboard)


def get_answer(message):
    a = users[message.chat.id]['min']
    b = users[message.chat.id]['max']
    number = randint(a, b)
    users[message.chat.id]['next'] = number
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_less = telebot.types.InlineKeyboardButton(text=f"Моё число меньше {number}",
                                                     callback_data='change_max')
    button_equal = telebot.types.InlineKeyboardButton(text=f"Ты прав, моё число {number}",
                                                      callback_data='game_over')
    button_more = telebot.types.InlineKeyboardButton(text=f"Моё число больше {number}",
                                                     callback_data='change_min')
    keyboard.row(button_less)
    keyboard.row(button_equal)
    keyboard.row(button_more)
    bot.send_message(message.chat.id,
                     f"Вы загадали число {number}?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'game_over')
def game_over(call):
    welcome(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'change_min')
def change_min(call):
    users[call.message.chat.id]['min'] = users[call.message.chat.id]['next'] + 1
    get_answer(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'change_max')
def change_max(call):
    users[call.message.chat.id]['max'] = users[call.message.chat.id]['next'] - 1
    get_answer(call.message)


bot.infinity_polling()