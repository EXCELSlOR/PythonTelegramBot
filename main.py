import telebot

bot = telebot.TeleBot('8181700980:AAFw-EsOg3F0CUdkyVETdLS5LqKMQbTOvew')


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