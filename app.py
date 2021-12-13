import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)




# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def messege_for_start(message: telebot.types.Message):

    text = 'Привет! Я бот, подскажу тебе курс валюты. Чтобы начать работу, введи команду в следующем формате (через пробел):\n<название валюты из которой переводим деньги> <в какую валюту нужно перевести> <количество переводимой валюты>' \
           '\n\nУвидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)

# Обработчик для видов валюты
@bot.message_handler(commands=['values'])
def message_for_values(message: telebot.types.Message):
    text = "Доступны следующие валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# Обрабатываются все сообщения text
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
    # Если пользователь ввел более 3х значений
        if len(values) != 3:
            raise APIException("Требуется указать 3 параметра")

        quote, base, amount = values
        result = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода со стороны пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # quote(валюта, цену, которой хотим узнать в нашей валюте) = евро,
        # base (валюта, в которой узнаем цену) = рубль,
        # amount (какое количество валюты переводим) = 1
        # Пример: евро рубль 1 = Цена 1 рубля = 83.07 евро
        text = f'Стоимость {amount} {quote} в {base} - {result}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

