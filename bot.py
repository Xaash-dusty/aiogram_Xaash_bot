from database import init_db
import asyncio
from aiogram import Bot, Dispatcher
# Импортируем наши роутеры из папки handlers
from handlers.survey import router as survey_router
from handlers.common import router as common_router
from handlers.cinema import router as cinema_router

# Токен бота
TOKEN = "8944612722:AAFqmQQkMp2JdUojwp83kFIjwCX6LeXmklk"

from aiogram.client.session.aiohttp import AiohttpSession

async def main():
    # 1. Сначала создаем/проверяем базу данных
    await init_db() 
    
    # 2. Чистая инициализация бота (УБРАЛИ ПРОКСИ)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # 3. Подключаем наши роутеры
    dp.include_router(survey_router)
    dp.include_router(cinema_router)
    dp.include_router(common_router)
    
    print("Бот успешно запущен в модульном режиме!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
