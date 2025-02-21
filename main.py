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
    less_button = telebot.types.InlineKeyboardButton(text=f"Моё число меньше {number}",
                                                     callback_data='change_max')
    equal_button = telebot.types.InlineKeyboardButton(text=f"Ты прав, моё число {number}",
                                                      callback_data='game_over')
    more_button = telebot.types.InlineKeyboardButton(text=f"Моё число больше {number}",
                                                     callback_data='change_min')
    keyboard.add(less_button)
    keyboard.row(equal_button)
    keyboard.row(more_button)
    bot.send_message(message.chat.id,
                     f"Вы загадали число {number}?",
                     reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'game_over')
def game_over(call):
    start_new_game(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'change_min')
def change_min(call):
    users[call.message.chat.id]['min'] = users[call.message.chat.id]['next'] + 1
    get_answer(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'change_max')
def change_max(call):
    users[call.message.chat.id]['max'] = users[call.message.chat.id]['next'] - 1
    get_answer(call.message)


bot.infinity_polling()
'''

def save_username(message):
    name = message.text
    users[message.chat.id]['name'] = name
    bot.send_message(message.chat.id, f'Отлично, {name}. Теперь укажи свою фамилию')
    bot.register_next_step_handler(message, save_surname)


def save_surname(message):
    users[message.chat.id]['surname'] = message.text
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
                                                     callback_data='save_data')
    button_change = telebot.types.InlineKeyboardButton(text="Изменить",
                                                       callback_data='change_data')
    keyboard.add(button_save, button_change)

    bot.send_message(message.chat.id, f'Сохранить данные?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'save_data')
def save_btn(call):
    message = call.message
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text='Данные сохранены!')


@bot.callback_query_handler(func=lambda call: call.data == 'change_data')
def save_btn(call):
    message = call.message
    message_id = message.message_id
    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text='Изменение данных!')
    write_to_support(message)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()




@bot.message_handler(commands=['start'])
def send_first_message(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Привет!", "Как дела?")
    bot.send_message(message.chat.id, "Я готов к общению",
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'],
                     func=lambda message: "привет" in message.text.strip().lower())
def send_hello_message(message):
    bot.send_message(message.from_user.id,
                     f"Привет, {message.from_user.first_name} {message.from_user.last_name}!")


@bot.message_handler(content_types=['text'],
                     func=lambda message: message.text.strip().lower() == "как дела?")
def send_how_are_you_message(message):
    bot.send_message(message.from_user.id, "Отлично, как твои дела?")


@bot.message_handler(content_types=['text'])
def not_understand_message(message):
    bot.send_message(message.from_user.id, "Прости, не понимаю тебя")

bot.polling(none_stop=True)
'''
