import aiohttp
from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

# Вставь сюда токен, который тебе выдал @kinopoiskdev_bot в Telegram
KINO_TOKEN = "F4X0R8F-DC54FNE-JA3SH7J-66V53KZ"

class MovieSearch(StatesGroup):
    waiting_for_title = State()

# 1. Запуск поиска фильма
@router.message(F.text.lower() == "киноман")
async def start_movie_search(message: types.Message, state: FSMContext):
    await state.set_state(MovieSearch.waiting_for_title)
    await message.answer("🎬 Введи название фильма (можно на русском, не обязательно точь-в-точь):")

# 2. Ловим название и стучимся в API Кинопоиска
@router.message(MovieSearch.waiting_for_title)
async def process_movie_title(message: types.Message, state: FSMContext):
    movie_title = message.text
    await state.clear() # Сбрасываем состояние
    
    # Мы используем домен .ru, который не вызывает сбоев у VPN-сервисов
    url = f"https://api.poiskkino.dev/v1.4/movie/search?query={movie_title}"



    
    # Для Кинопоиска токен нужно передавать в "заголовках" (Headers), а не в самой ссылке
    headers = {
        "X-API-KEY": KINO_TOKEN
    }
    
    async with aiohttp.ClientSession() as session:
        # Делаем запрос, передавая заголовки с токеном
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            
            # Извлекаем список найденных фильмов (Кинопоиск возвращает список в ключе 'docs')
            movies = data.get("docs", [])
            
            if not movies:
                await message.answer("❌ Фильм не найден! Попробуй ввести по-другому.")
                return
            
            # Берем самый первый, наиболее подходящий фильм из списка результатов
            best_match = movies[0]
            
            # Вытаскиваем русские данные
            title = best_match.get("name") or best_match.get("alternativeName") or "Без названия"
            year = best_match.get("year") or "Год неизвестен"
            rating = best_match.get("rating", {}).get("kp") or "Нет оценки" # Рейтинг Кинопоиска
            plot = best_match.get("description") or "Описание отсутствует."
            
            # Вытаскиваем ссылку на постер (картинку)
            poster_url = best_match.get("poster", {}).get("url")
            
            # Ограничиваем слишком длинное описание, чтобы Telegram не выдал ошибку
            if len(plot) > 600:
                plot = plot[:600] + "..."
                
            # Округляем рейтинг до одного знака после запятой, если это число
            if isinstance(rating, (int, float)):
                rating = round(rating, 1)

            # Форматируем красивый текст
            caption_text = (
                f"🎬 **{title}** ({year})\n\n"
                f"⭐ Рейтинг Кинопоиска: {rating}/10\n\n"
                f"📝 **Сюжет:** {plot}"
            )

            
            # Отправляем результат
            if poster_url:
                await message.answer_photo(photo=poster_url, caption=caption_text, parse_mode="Markdown")
            else:
                await message.answer(text=caption_text, parse_mode="Markdown")
