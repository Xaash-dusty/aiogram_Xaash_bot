from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# 1. Создаем роутер для анкеты
router = Router()

# 2. Сама структура анкеты
class Form(StatesGroup):
    name = State()
    city = State()

# 3. Шаг первый: Ловим имя
@router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await state.set_state(Form.city)
    await message.answer("Принято! А из какого ты города?")

# 4. Шаг второй: Ловим город
@router.message(Form.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(user_city=message.text)
    user_data = await state.get_data()
    
    name = user_data.get("user_name")
    city = user_data.get("user_city")
    await state.clear()
    
    await message.answer(f"Приятно познакомиться, {name} из города {city}! Анкета успешно заполнена. 🎉")
