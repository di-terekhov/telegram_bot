import time
import requests
import telebot
from telebot import types

api_key = 'b97ea0d7-8c57-4af8-9116-15adac8ce0f5'  # Your api from pro.coinmarketcap.com
bot_key = '5062337339:AAEipbuaOA2Im3dc0yaSXfIGQLVh5abQav8'  # Your bot key

bot = telebot.TeleBot(bot_key)
currency = 'ETH'  # set up the name of the currency
time_gap = 2 * 60  # set up the gap between rate checking (in seconds)
currency_converter = 'USD'  # Currency code (ISO 4217)
flag = False


@bot.message_handler(commands=['start'])
def start_bot(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_btn = types.KeyboardButton("Start")
    stop_btn = types.KeyboardButton("Stop")

    markup.add(start_btn, stop_btn)

    bot.send_message(message.chat.id,
                     "Howdy, {0.first_name}!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

    bot.send_message(message.chat.id, f"I am tracking the rate of cryptocurrency {currency}, with an"
                                      f" interval of {round(time_gap / 60, 2)} minutes.\n"
                                      f"For start push the button below ")


def get_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '50',
        'convert': currency_converter
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers, params=parameters).json()
    # Here you can choose your currency btc_price = response['data'][X],
    # where X = currency number(0 - BTC, 1 - ETH, etc.)
    btc_price = response['data'][1]['quote'][currency_converter]['price']
    answer = f'{currency} price is {round(btc_price)} {currency_converter}'
    return answer


@bot.message_handler(content_types=['text'])
def commands(message):
    global flag, time_gap
    if message.chat.type == 'private':

        if message.text == 'Start':
            flag = False

            def main():
                while True:
                    if flag:
                        break
                    price = get_price()
                    print(price)
                    bot.send_message(message.chat.id, price)
                    time.sleep(time_gap)

            main()
        elif message.text == 'Stop':
            flag = True
            bot.send_message(message.chat.id, f"Bot has been stopped")


# RUN
bot.polling(none_stop=True)
