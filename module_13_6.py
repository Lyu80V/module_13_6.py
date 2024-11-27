from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = '7201079216:AAGijMIsykxlS74Osg113pM0mFLkBVyn9Wo'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()     # возраст
    growth = State()  # рост
    weight = State()  # вес
    gender = State()  # пол

m_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
m_kb.row(button, button2)

kb = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.row(button3, button4)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=m_kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await  message.answer('Выберите опцию:', reply_markup=kb)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('(10 * вес + 6.25 * рост - 5 * возраст + 5) - для мужчин, '
                              '\n(10 * вес + 6.25 * рост - 5 * возраст - 161) - для женщин')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст(г):')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост(см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес(кг):')
    await UserState.weight.set()

# @dp.message_handler(state=UserState.weight)
# async def set_gender(message, state):
#     await state.update_data(weight=message.text)
#     await message.answer('Введите свой пол(муж/жен):')
#     await UserState.gender.set()
#
# @dp.message_handler(state=UserState.gender)
# async def send_calories(message, state):
#     await state.update_data(gender=message.text)
#     data = await state.get_data()
#     if state.update_data(gender='муж'):
#         norma_1 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)  # для мужчин
#         await message.answer(f'Ваша норма колорий:\n {norma_1} ккал')
#       #await state.finish()
#     else:
#         norma_2 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)  # для женщин
#         await message.answer(f'Ваша норма колорий: {norma_2} ккал')
#     await state.finish()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma_1 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)    # для мужчин
    norma_2 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)  # для женщин
    await message.answer(f'Ваша норма колорий:\n {norma_1} ккал - для мужчин \n {norma_2} ккал - для женщин ')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)