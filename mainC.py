import telebot
from telebot import types
import time

bot = telebot.TeleBot('8336228498:AAHISNf60yOS0NcbDzZnx476M5VFJbg2HEA')

# 1. БАЗА ДАННЫХ
score = 0
quiz_data = [
    {"question": "Какая планета самая большая?", "options": ["Марс", "Юпитер", "Сатурн"], "correct": "Юпитер"},
    {"question": "Сколько полосок на флаге США?", "options": ["10", "13", "15"], "correct": "13"},
    {"question": "Какой язык программирования мы учим?", "options": ["Java", "Python", "C++"], "correct": "Python"}
]

# 2. ФУНКЦИЯ-ПОМОЩНИК (Отрисовка вопроса)
def show_question(message, q_index):
    q = quiz_data[q_index]
    markup = types.InlineKeyboardMarkup()
    
    for option in q['options']:
        # Хитрый callback_data: "индекс_вопроса|ответ"
        markup.add(types.InlineKeyboardButton(option, callback_data=f"{q_index}|{option}"))
    
    bot.send_message(message.chat.id, q['question'], reply_markup=markup)

# 3. ОБРАБОТЧИК КОМАНДЫ /START
@bot.message_handler(commands=['start'])
def start(message):
    show_question(message, 0)

# 4. ОБРАБОТЧИК НАЖАТИЙ (Проверка ответа)
@bot.callback_query_handler(func=lambda call: True)
def check_answer(call):
    bot.answer_callback_query(call.id)
    
    global score
    # Разделяем данные из кнопки обратно на индекс и ответ
    # Было "0|Юпитер" -> станет q_index = 0, user_answer = "Юпитер"
    data = call.data.split('|')
    q_index = int(data[0])
    user_answer = data[1]
    
    correct_answer = quiz_data[q_index]['correct']

    if user_answer == correct_answer:
        text = f"✅ Верно! {user_answer}"
        score += 1
    else:
        text = f"❌ Ошибка! Правильно: {correct_answer}"
    next_index = q_index + 1
    # Редактируем сообщение, показывая результат
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text=text)
    if next_index < len(quiz_data):
        time.sleep(2) 
        show_question(call.message, next_index)
    else:
        bot.send_message(call.message.chat.id, f"🏁 Викторина окончена! Очков: {score} из {len(quiz_data)}")
        score = 0
    
    # ТУТ БУДЕТ ГЛАВНОЕ ЗАДАНИЕ (переход к следующему вопросу)
print('Bot go')
bot.infinity_polling()
