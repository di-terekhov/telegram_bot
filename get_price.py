import time
import requests
import telebot


api_key = '#########' # Your api from pro.coinmarketcap.com
bot_key = '#########' # Your bot key
chat_id = '#########' # Your telegram id
bot = telebot.TeleBot(bot_key)

currency = 'ETH' # set up the name of the currency
time_gap = 2 * 60 # set up the gap between rate checking (in seconds)
currency_converter = 'USD' # Currency code (ISO 4217)


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, f"Howdy, i am tracking the rate of cryptocurrency {currency}, with an"
                      f" interval of {round(time_gap/60, 2)} minutes ")


bot.polling()


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
    #Here you can choose your currency btc_price = response['data'][X], where X = currency number(0 - BTC, 1 - ETH, etc.)
    btc_price = response['data'][1]['quote'][currency_converter]['price']
    answer = f'{currency} price is {round(btc_price)} {currency_converter}'
    return answer


def main():
    while True:
        price = get_price()
        # print(price)
        bot.send_message(chat_id, price)
        time.sleep(time_gap)
main()



