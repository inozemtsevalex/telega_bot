import telebot
from extensions import APIException, Convertor
from token_cfg import TOKEN, currency

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду следующего вида:\n \
<имя валюты, цену которой вы хотите узнать>\n \
<имя валюты, в которой надо узнать цену первой валюты>\n \
<количество первой валюты>\n \
Чтобы увидеть перечень доступных валют введите команду /values"

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
   values = message.text.split(' ')
   try:
       if len(values) != 3:
           raise APIException('Неверное количество параметров!')
       answer = Convertor.get_price(*values)
   except APIException as e:
       bot.reply_to(message, f"Ошибка в команде:\n{e}")
   else:
       bot.reply_to(message, answer)

bot.polling(none_stop=True)