import asyncio
import os
from aiogram import Bot, Dispatcher
from database import init_db
from handlers.survey import router as survey_router
from handlers.common import router as common_router
from handlers.cinema import router as cinema_router

# Подключаем встроенную в python библиотеку для веб-серверов
from aiohttp import web

# Токен бота
TOKEN = "8944612722:AAFqmQQkMp2JdUojwp83kFIjwCX6LeXmklk"

# Специальная функция-заглушка для Render.com
# Когда Render или Cron-Job будут заходить на нашу страницу, мы будем отвечать "OK"
async def handle_render_ping(request):
    return web.Response(text="Бот успешно работает 24/7!")

async def main():
    # 1. Сначала создаем/проверяем базу данных
    await init_db() 
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    # 3. Подключаем наши роутеры
    dp.include_router(survey_router)
    dp.include_router(cinema_router)
    dp.include_router(common_router)
    
    print("Бот успешно запущен в модульном режиме!")
    
    # --- НАЧАЛО БЛОКА ДЛЯ RENDER.COM ---
    # Создаем мини-веб-сервер внутри бота
    app = web.Application()
    app.router.add_get("/", handle_render_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render выдает нам специальный секретный порт (PORT) в переменной среды.
    # Если её нет, ставим стандартный для Render порт 10000.
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    # Запускаем сайт в фоновом режиме, чтобы он не мешал работе кнопок бота
    await site.start()
    print(f"Мини-веб-сервер для Render запущен на порту {port}")
    # --- КОНЕЦ БЛОКА ДЛЯ RENDER.COM ---

    # Запускаем бесконечный опрос Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
