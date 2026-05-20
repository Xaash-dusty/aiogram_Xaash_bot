import telebot
from telebot import types
import random

bot = telebot.TeleBot('8336228498:AAEBXOpuTyy-ACrXqvUKYvq-J8j5CaoJ86o')

@bot.message_handler(commands=['start'])
def start(message):
    # Создаем инлайн-клавиатуру
    markup = types.InlineKeyboardMarkup()
    
    # Создаем кнопки (url - откроет ссылку, callback_data - отправит сигнал боту)
    btn_site = types.InlineKeyboardButton("Перейти на сайт", url="https://google.com")
    btn_help = types.InlineKeyboardButton("Помощь", callback_data="help")
    btn_info = types.InlineKeyboardButton("О боте", callback_data="info")
    
    markup.add(btn_site, btn_help, btn_info)
    
    bot.send_message(message.chat.id, "Выбери действие под этим сообщением:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text(message):
    # Печатаем в консоль, чтобы видеть, что бот живой
    print(f"Пришло сообщение: {message.text}")
    
    if message.text == "Как дела?":
        mood_list=["Грущу...", "Летаю!", "Нормально"]
        bot.send_message(message.chat.id, f"{random.choice(mood_list)}")
    
    elif message.text == "Случайное число":
        num = random.randint(1, 100)
        bot.send_message(message.chat.id, f"Твое счастливое число: {num}")
    
    elif message.text == "Покажи котика":
        bot.send_photo(message.chat.id, "https://cataas.com")
    
    elif message.text == "Бросить кости":
        numk = random.randint(1, 6)
        bot.send_message(message.chat.id, f"Выпало число: {numk}")
        
    else:
        bot.send_message(message.chat.id, f" {message.from_user.first_name}, я не знаю команды'{message.text}'.Пользуйся кнопками! ")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Проверяем, какая кнопка нажата
    if call.data == "help":
        # Редактируем старое сообщение, чтобы показать текст помощи
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Тут будет инструкция по боту!")
    elif call.data == "info":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Я создан Савелием!")
    bot.answer_callback_query(call.id, text="Уведомление прочитано!", show_alert=False)
    #^^^bot.answer_callback_query(call.id)

print("Бот обновлен и запущен!")
# none_stop=True поможет боту не вылетать при сбоях связи
bot.infinity_polling(none_stop=True)
