from database import add_user, get_users_count, get_all_users
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, InlineKeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext

# Импортируем нашу анкету из соседнего файла для запуска
from handlers.survey import Form 

# Создаем роутер для общих команд
router = Router()
ADMIN_ID = 7106093310

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    # Сохраняем пользователя в SQLite!
    await add_user(user_id=message.from_user.id, username=message.from_user.username)

    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Привет"), KeyboardButton(text="Хозяин"),
                KeyboardButton(text="Об авторе"), KeyboardButton(text="Киноман"),
                KeyboardButton(text="Помощь"))
    builder.adjust(2)
    await message.answer("Привет! Выбери действие на кнопках ниже:", reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для выполнения этой команды! 🚫")
        return # Выходим из функции, чтобы код ниже не выполнялся
    
    count = await get_users_count()
    users = await get_all_users()

    # Собираем красивый текстовый список
    users_list = ""
    for user in users:
        user_id = user[0]
        username = user[1] if user[1] else "Нет никнейма"
        users_list += f"• ID: `{user_id}` — @{username}\n"

    await message.answer(
        f"📊 **Панель администратора**\n"
        f"Всего пользователей в базе: {count}\n\n"
        f"**Список пользователей:**\n{users_list}"
    )


@router.message(or_f(Command("help"), F.text.lower() == "помощь"))
async def cmd_help(message: types.Message):
    inline_builder = InlineKeyboardBuilder()
    inline_builder.add(
        InlineKeyboardButton(text="📄 Получить документ", callback_data="get_doc"),
        InlineKeyboardButton(text="🎵 Получить музыку", callback_data="get_track"),
        InlineKeyboardButton(text="⭕ Получить кругляшок", callback_data="get_round"),
        InlineKeyboardButton(text="ℹ️ Узнать секрет", callback_data="secret_pressed"),
        InlineKeyboardButton(text="🎁 Получить подарок", callback_data="get_gift"),
        InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")
    )
    inline_builder.adjust(2)
    await message.answer("Выбери действие:", reply_markup=inline_builder.as_markup())

# --- Все твои callback_query обработчики ---
@router.callback_query(lambda call: call.data == "secret_pressed")
async def secret_button(callback: types.CallbackQuery):
    await callback.answer()
    back_builder = InlineKeyboardBuilder()
    back_builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_help"))
    await callback.message.edit_text(text="Секрет прост: пиши код каждый день вместе со мной! 🚀", reply_markup=back_builder.as_markup())

@router.callback_query(lambda call: call.data == "back_to_help")
async def back_to_help(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cmd_help(callback.message) # Просто вызываем функцию помощи

@router.callback_query(lambda call: call.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cmd_start(callback.message) # Просто вызываем функцию меню

@router.callback_query(lambda call: call.data == "show_contacts")
async def show_contacts(callback: types.CallbackQuery):
    await callback.answer()
    back_builder = InlineKeyboardBuilder()
    back_builder.add(InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu"))
    await callback.message.edit_text(text="Связаться с автором: @Xaash_dusty", reply_markup=back_builder.as_markup())

@router.callback_query(lambda call: call.data == "get_gift")
async def get_gift(callback: types.CallbackQuery):
    await callback.answer()
    back_builder = InlineKeyboardBuilder()
    back_builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_help"))
    await callback.message.edit_text(text="Подарок получен ✅") 
    await callback.message.answer_photo(photo=FSInputFile("face.png"), caption="А вот и твой подарок! 🎁", reply_markup=back_builder.as_markup())

@router.callback_query(lambda call: call.data == "get_doc")
async def send_document(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_document(document=FSInputFile("document.txt"), caption="Вот твой текстовый документ! 📄")

@router.callback_query(lambda call: call.data == "get_track")
async def send_audio(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_audio(audio=FSInputFile("music.mp3"), caption="Слушай отличный трек! 🎵")

@router.callback_query(lambda call: call.data == "get_round")
async def send_round_video(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer_video_note(video_note=FSInputFile("video_note.mp4"))

# --- Эхо и запуск FSM ---
@router.message()
async def echo_message(message: types.Message, state: FSMContext):
    user_text = message.text.lower()
    if user_text == 'привет':
        await state.set_state(Form.name)
        await message.answer("Отлично, давай заполним анкету! Как тебя зовут?")
    elif 'хозяин' in user_text:
        await message.answer_photo(photo="https://picsum.photos", caption="Мой хозяин — Xaash! 🖼️")
    elif user_text == 'об авторе':
        inline_builder = InlineKeyboardBuilder()
        inline_builder.add(InlineKeyboardButton(text="Показать контакты", callback_data="show_contacts"))
        await message.answer(text="Этого бота создал Я!", reply_markup=inline_builder.as_markup())
    else:
        await message.answer(f"Ты написал мне: {message.text}, но я тебя не понял /help")
