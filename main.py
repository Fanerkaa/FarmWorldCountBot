import telebot
import config
from telebot import types
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Цена на ресурсы")
    btn2 = types.KeyboardButton("Узнать цену TON 💎")
    btn3 = types.KeyboardButton("Посчитать количество TON 💎")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, "👋 Привет! Я Бот помощник по проекту Farm World!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Цена на ресурсы':
        bot.send_message(message.from_user.id, f'🪵 1 Дерево - {config.wood} TON 💎\n🍖 1 Мясо - {config.meat} TON 💎\n💰 1 Золото - {config.gold} TON 💎', parse_mode='Markdown')

    elif message.text == 'Узнать цену TON 💎':
        # Отправляем запрос к сайту CoinMarketCap для получения данных о криптовалюте TON
        response = requests.get('https://coinmarketcap.com/ru/currencies/toncoin/')
        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим информацию о курсе криптовалюты TON на странице
        data_group = soup.find('span', {'class': 'sc-65e7f566-0 clvjgF base-text'})
        if data_group:
            TON_crypto_value = data_group.text
            TON_crypto_equivalent = float(TON_crypto_value.replace('₽', ''))
            bot.send_message(message.from_user.id, f'💎 TON : {TON_crypto_equivalent} RUB')
        else:
            bot.send_message(message.from_user.id, "Невозможно получить актуальный курс TON криптовалюты")

    elif message.text == 'Посчитать количество TON 💎':
        bot.send_message(message.from_user.id, "Введите количество дерева, мяса и золота в формате: Дерево/Мясо/Золото")

    else:
        calculate_ton(message)

def calculate_ton(message):
    if "/" in message.text:
        resources = message.text.split("/")
        if len(resources) == 3:
            try:
                tree = float(resources[0])
                meat = float(resources[1])
                gold = float(resources[2])
                total_ton = tree * config.wood + meat * config.meat + gold * config.gold
                bot.send_message(message.from_user.id, f"Общее количество TON 💎: {total_ton}")
            except ValueError:
                bot.send_message(message.from_user.id, "Пожалуйста, введите числовые значения для количества ресурсов.")
        else:
            bot.send_message(message.from_user.id, "Пожалуйста, введите количество дерева, мяса и золота в формате: Дерево/Мясо/Золото")
    else:
        bot.send_message(message.from_user.id, "Пожалуйста, введите количество дерева, мяса и золота в формате: Дерево/Мясо/Золото")

bot.polling(none_stop=True, interval=0)
