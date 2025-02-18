import telebot

bot = telebot.TeleBot('8181700980:AAFw-EsOg3F0CUdkyVETdLS5LqKMQbTOvew')


@bot.message_handler(content_types=['text'])
def resend_text_messages(message):
    if "привет" in message.text.strip().lower():
        bot.send_message(message.from_user.id,
                         f"Привет, {message.from_user.first_name} {message.from_user.last_name}!")
    elif message.text.strip().lower() == "как дела?":
        bot.send_message(message.from_user.id, "Отлично, как твои дела?")


bot.polling(none_stop=True)