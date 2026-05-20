import telebot
from telebot import types
from pycbrf import ExchangeRates
from datetime import datetime

bot = telebot.TeleBot('8336228498:AAHISNf60yOS0NcbDzZnx476M5VFJbg2HEA')

# Глобальная переменная
convert = 'usd' 

def get_rates():
    rates = ExchangeRates(datetime.now())
    usd = rates['USD'].value
    eur = rates['EUR'].value
    return usd, eur

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🇺🇸 Курс USD")
    btn2 = types.KeyboardButton("🇪🇺 Курс EUR")
    btn3 = types.KeyboardButton("📊 Оба сразу")
    btn4 = types.KeyboardButton("🔄 Перевод в EUR") # Сократил название для кнопки
    btn5 = types.KeyboardButton("🏠 В меню")
    markup.add(btn1, btn2, btn3)
    markup.add(btn4, btn5)
    
    bot.send_message(message.chat.id, "Выбери валюту или введи число для перевода в USD:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global convert # ОБЯЗАТЕЛЬНО! Позволяет менять переменную вне функции

    if message.text == "🏠 В меню":
        convert = 'usd' # Сбрасываем режим на доллары при возврате
        start(message)
        return
    
    elif message.text == "🔄 Перевод в EUR":
        convert = 'eur'
        bot.send_message(message.chat.id, "Режим изменен: теперь вводи число для перевода в ЕВРО 🇪🇺")
        return

    try:
        usd, eur = get_rates()

        if message.text.isdigit():
            if convert == 'eur':
                result = int(message.text) / eur
                bot.send_message(message.chat.id, f"{message.text} руб. = {round(result, 2)} EUR 💶")
            else:
                result = int(message.text) / usd
                bot.send_message(message.chat.id, f"{message.text} руб. = {round(result, 2)} USD 💵")

        elif message.text == "🇺🇸 Курс USD":
            bot.send_message(message.chat.id, f"💵 Доллар: {usd} руб.")
            
        elif message.text == "🇪🇺 Курс EUR":
            bot.send_message(message.chat.id, f"💶 Евро: {eur} руб.")
            
        elif message.text == "📊 Оба сразу":
            bot.send_message(message.chat.id, f"🇺🇸 USD: {usd} руб.\n🇪🇺 EUR: {eur} руб.")
            
        else:
            bot.send_message(message.chat.id, "Нажми на кнопку или введи число! 👇")
            
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка связи с банком 🏦")

print("Бот-валютчик запущен!")
bot.infinity_polling(none_stop=True)
