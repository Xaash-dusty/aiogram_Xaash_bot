import telebot
from telebot import types
import os

bot = telebot.TeleBot('8336228498:AAHISNf60yOS0NcbDzZnx476M5VFJbg2HEA')

def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(task + "\n")
            
def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    return []

# ШАГ 1: Загружаем задачи из файла сразу при запуске
tasks = load_tasks()
            
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("➕ Добавить задачу")
    btn2 = types.KeyboardButton("📋 Мои задачи")
    btn3 = types.KeyboardButton("🗑 Очистить список")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Это твой менеджер задач. Что сделаем?", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_tasks(message):
    if message.text == "➕ Добавить задачу":
        bot.send_message(message.chat.id, "Просто напиши текст задачи следующим сообщением.")
    
    elif message.text == "📋 Мои задачи":
        if not tasks:
            bot.send_message(message.chat.id, "Твой список задач пока пуст! ✨")
        else:
            display_text = "Твои дела:\n"
            for i, t in enumerate(tasks, start=1):
                display_text += f"{i}. {t}\n"
            bot.send_message(message.chat.id, f"{display_text}\nВсего задач: {len(tasks)}")
            
    elif message.text == "🗑 Очистить список":
        tasks.clear()
        save_tasks() # ШАГ 2.1: Сохраняем пустоту
        bot.send_message(message.chat.id, "Список очищен! 🧹")
    
    else:
        if message.text.isdigit():
            number = int(message.text)
            if 0 < number <= len(tasks):
                removed = tasks.pop(number - 1)
                save_tasks() # ШАГ 2.2: Сохраняем после удаления
                bot.send_message(message.chat.id, f"Задача '{removed}' удалена! ✅")
            else:
                bot.send_message(message.chat.id, "Задачи с таким номером нет!")
        
        else:
            if len(message.text) < 50:
                tasks.append(message.text)
                save_tasks() # ШАГ 2.3: Сохраняем после добавления
                bot.send_message(message.chat.id, f"Добавлено: {message.text} ✅")
            else:
                bot.send_message(message.chat.id, "Слишком длинное описание!")

print("Менеджер задач запущен!")
bot.infinity_polling(none_stop=True)
