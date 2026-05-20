import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


# Создаем группу состояний для нашей анкеты
class Form(StatesGroup):
    name = State()  # Шаг 1: Ожидание имени
    city = State()  # Шаг 2: Ожидание города

# 1. Токен бота (получи у @BotFather в Telegram)
TOKEN = "8944612722:AAFqmQQkMp2JdUojwp83kFIjwCX6LeXmklk"

# 2. Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 3. Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # 1. Создаем строителя кнопок
    builder = ReplyKeyboardBuilder()
    
    # 2. Добавляем кнопки в строитель
    builder.add(KeyboardButton(text="Привет"))
    builder.add(KeyboardButton(text="Хозяин"))
    builder.add(KeyboardButton(text="Об авторе"))
    builder.add(KeyboardButton(text="Помощь"))
    
    # 3. Делаем так, чтобы кнопки шли красиво (например, по 2 штуки в ряд)
    builder.adjust(2)
    
    # 4. Отправляем сообщение и прикрепляем созданную клавиатуру
    await message.answer(
        "Привет! Выбери действие на кнопках ниже: /help",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.message(or_f(Command("help"), F.text.lower() == "помощь"))
async def cmd_help(message: types.Message):

    # 1. Создаем строителя ИНЛАЙН кнопок
    inline_builder = InlineKeyboardBuilder()
    
    # 2. Добавляем inline-кнопку с ЗАШИФРОВАННЫМ сигналом (callback_data)
    inline_builder.add(InlineKeyboardButton(text="📄 Получить документ", callback_data="get_doc"  ))
    inline_builder.add(InlineKeyboardButton(text="🎵 Получить музыку", callback_data="get_track"  ))
    inline_builder.add(InlineKeyboardButton(text="⭕ Получить кругляшок", callback_data="get_round"  ))

    inline_builder.add(InlineKeyboardButton(text="ℹ️ Узнать секрет", callback_data="secret_pressed"  ))
    inline_builder.add(InlineKeyboardButton(text="🎁 Получить подарок", callback_data="get_gift"  ))
    inline_builder.add(InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu"  ))
    inline_builder.adjust(2)
    # 3. Отправляем сообщение с inline-клавиатурой
    await message.answer(
        "Выбери: узнать секрет обучения, открыть файл или получить подарок?",
        reply_markup=inline_builder.as_markup()
    )

@dp.callback_query(lambda call: call.data == "secret_pressed")
async def secret_button(callback: types.CallbackQuery):
    await callback.answer()
    
    # Создаем новую кнопку для шага назад
    back_builder = InlineKeyboardBuilder()
    back_builder.add(InlineKeyboardButton(
        text="🔙 Назад", 
        callback_data="back_to_help"  # Новый скрытый шифр!
    ))
    
    # Изменяем и текст, и клавиатуру!
    await callback.message.edit_text(
        text="Секрет прост: пиши код каждый день вместе со мной! 🚀",
        reply_markup=back_builder.as_markup()
    )

@dp.callback_query(lambda call: call.data == "back_to_help")
async def back_to_help(callback: types.CallbackQuery):
    await callback.answer()
    
    # 1. Создаем строителя ИНЛАЙН кнопок
    inline_builder = InlineKeyboardBuilder()
    
    # 2. Добавляем inline-кнопку с ЗАШИФРОВАННЫМ сигналом (callback_data)
    inline_builder.add(InlineKeyboardButton(text="📄 Получить документ", callback_data="get_doc"  ))
    inline_builder.add(InlineKeyboardButton(text="🎵 Получить музыку", callback_data="get_track"  ))
    inline_builder.add(InlineKeyboardButton(text="⭕ Получить кругляшок", callback_data="get_round"  ))

    inline_builder.add(InlineKeyboardButton(text="ℹ️ Узнать секрет", callback_data="secret_pressed"  ))
    inline_builder.add(InlineKeyboardButton(text="🎁 Получить подарок", callback_data="get_gift"  ))
    inline_builder.add(InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu"  ))
    inline_builder.adjust(2)
    
    await callback.message.delete()
    # Возвращаем исходный текст и кнопку
    await callback.message.answer(
        text="Выбери: узнать секрет обучения, открыть файл или получить подарок?",
        reply_markup=inline_builder.as_markup()
    )

@dp.callback_query(lambda call: call.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    # 1. Гасим часики на кнопке
    await callback.answer()
    
    # 2. Удаляем старое сообщение (неважно, текст это был или фото!)
    await callback.message.delete()
    
    # 3. Создаем заново Reply-кнопки
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Привет"))
    builder.add(KeyboardButton(text="Хозяин"))
    builder.add(KeyboardButton(text="Об авторе"))
    builder.add(KeyboardButton(text="Помощь"))
    builder.adjust(2)
    
    # 4. Отправляем СВЕЖЕЕ сообщение в чат и возвращаем нижние кнопки
    await callback.message.answer(
        "Вы вернулись в главное меню. Выбери действие ниже: /help",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@dp.callback_query(lambda call: call.data == "show_contacts")
async def show_contacts(callback: types.CallbackQuery):
    # 1. Гасим часики на кнопке
    await callback.answer()
    
    back_builder = InlineKeyboardBuilder()
    back_builder.add(InlineKeyboardButton(
        text="Назад в меню", 
        callback_data="back_to_menu"  # Новый скрытый шифр!
    ))

    # 2. Убираем инлайн-кнопки у старого сообщения, чтобы они не висели зря
    await callback.message.edit_text(
        text="Связаться с автором: @Xaash_dusty",
        reply_markup=back_builder.as_markup()
    ) 

@dp.callback_query(lambda call: call.data == "get_gift")
async def get_gift(callback: types.CallbackQuery):
    # 1. Гасим часики анимации клика
    await callback.answer()
    
    # 2. Создаем кнопку "Назад в меню"
    back_builder = InlineKeyboardBuilder()
    back_builder.add(InlineKeyboardButton(
        text="🔙 Назад", 
        callback_data="back_to_help"
    ))
    
    # 3. Меняем старый текст на "Подарок получен"
    await callback.message.edit_text(text="Подарок получен ✅") 

    # 4. Правильная ссылка на картинку с размером
    local_photo = FSInputFile("face.png")
    
    # 5. ИСПРАВЛЕНО: Отправляем фото через callback.message
    await callback.message.answer_photo(
        photo=local_photo,
        caption="А вот и твой подарок! 🎁",
        reply_markup=back_builder.as_markup()
    )

# 1. Обработчик для отправки ДОКУМЕНТА
@dp.callback_query(lambda call: call.data == "get_doc")
async def send_document(callback: types.CallbackQuery):
    await callback.answer() # Гасим часики
    
    # Указываем путь к локальному файлу
    local_doc = FSInputFile("document.txt")
    
    # Отправляем документ с подписью
    await callback.message.answer_document(document=local_doc, caption="Вот твой текстовый документ! 📄"  )

# 2. Обработчик для отправки МУЗЫКИ
@dp.callback_query(lambda call: call.data == "get_track")
async def send_audio(callback: types.CallbackQuery):
    await callback.answer() # Гасим часики
    
    # Указываем путь к музыкальному файлу
    local_audio = FSInputFile("music.mp3")
    
    # Отправляем аудиофайл
    await callback.message.answer_audio(audio=local_audio, caption="Слушай отличный трек! 🎵"  )

# 3. Обработчик для отправки КРУГЛЯШКА
@dp.callback_query(lambda call: call.data == "get_round")
async def send_round_video(callback: types.CallbackQuery):
    await callback.answer() # Гасим часики
    
    # Указываем путь к круглому видео
    local_video = FSInputFile("video_note.mp4")
    
    # Отправляем видеозаметку
    await callback.message.answer_video_note(
        video_note=local_video
    )

# 1. Ловим ответ, когда бот находится строго в состоянии Form.name
@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    # Сохраняем введенный текст (имя) в виртуальный блокнот
    await state.update_data(user_name=message.text)
    
    # Переводим пользователя на следующий шаг — ожидание города
    await state.set_state(Form.city)
    
    # Задаем второй вопрос
    await message.answer("Принято! А из какого ты города?")

# 2. Ловим ответ, когда бот находится строго в состоянии Form.city
@dp.message(Form.city)
async def process_city(message: types.Message, state: FSMContext):
    # Сохраняем введенный город в блокнот
    await state.update_data(user_city=message.text)
    
    # Достаем ВСЕ сохраненные данные из блокнота
    user_data = await state.get_data()
    
    # Записываем данные в удобные переменные
    name = user_data.get("user_name")
    city = user_data.get("user_city")
    
    # Обязательно ЗАВЕРШАЕМ анкету (очищаем состояние памяти), 
    # чтобы бот снова стал обычным и реагировал на команды
    await state.clear()
    
    # Выводим финальный результат
    await message.answer(f"Приятно познакомиться, {name} из города {city}! Анкета успешно заполнена. 🎉")

@dp.message()
async def echo_message(message: types.Message, state: FSMContext):
    # message.text — это сам текст, который прислал пользователь
    user_text = message.text.lower()
    if user_text == 'привет':
        # 1. Переводим пользователя в состояние ожидания имени
        await state.set_state(Form.name)
        
        # 2. Задаем первый вопрос
        await message.answer("Отлично, давай заполним анкету! Как тебя зовут?")

    elif 'хозяин' in user_text:
        # Ссылка на любую картинку из интернета
        photo_url = "https://picsum.photos" 
        
        # Вместо .answer() используем .answer_photo()
        await message.answer_photo(
            photo=photo_url,
            caption="Мой хозяин — Xaash! А это случайная красивая картинка для тебя 🖼️"
        )

    elif user_text == 'об авторе':
        inline_builder = InlineKeyboardBuilder()
        inline_builder.add(InlineKeyboardButton(
            text="Показать контакты", 
            callback_data="show_contacts"
        ))

        # Возвращаем исходный текст и кнопку
        await message.answer(
            text="Этого бота создал Я!",
            reply_markup=inline_builder.as_markup()
        )
    else:
        await message.answer(f"Ты написал мне: {message.text}, но я тебя не понял /help")

# 4. Главная функция запуска бота
async def main():
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
