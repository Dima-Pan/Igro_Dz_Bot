import logging
from random import*
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

logging.basicConfig(level=logging.INFO)

API_TOKEN = config('API_TOKEN')
bot = Bot(token=API_TOKEN)
storeg = MemoryStorage()
dp = Dispatcher(bot, storage=storeg)

keyboard = types.ReplyKeyboardMarkup()
btn_1 = types.KeyboardButton('Да!!!!!!')
btn_2 = types.KeyboardButton('Нет.')
keyboard.add(btn_1, btn_2)

class igrobot(StatesGroup):
    start = State() 
    task = State()

count_wrong = []  
count_right = [] 
count = []
primer = []

def prime():
    primer.clear()
    a = f'{randint(1, 100)} {choice(["+", "-", "/", "*"])} {randint(1, 100)}'
    primer.append(a)
    return a

@dp.message_handler(commands=['stop_game'], state='*')
async def end(message: types.Message, state: FSMContext):
    primer.clear()
    await message.answer(f"Вы решили {len(count)} примеров\nПравильно {len(count_right)}\nНеправильно {len(count_wrong)}\nПриходи когда хочешь занятся матешой")

@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply("Hi!\nЯ бот для игры с примерами!\nПравила: Ваша задача правильно ответить на пример!\nДля окончания игрв напишите /stop_game\nВы готовы начать?", reply_markup=keyboard)
    await igrobot.start.set()
    count_wrong.clear()
    count_right.clear()
    count.clear()
    
@dp.message_handler(state=igrobot.start)
async def echo(message: types.Message, state: FSMContext):
    if message.text == 'Да!!!!!!':
        await message.reply('Ура! Тогда начинаем😁', reply_markup=types.ReplyKeyboardRemove())
        c = prime()
        await message.answer(f'{c} =')
        await igrobot.task.set()
    else:
        await message.reply('Станет скучно, приходи!', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()

@dp.message_handler(state=igrobot.task)
async def otvet(message: types.Message, state: FSMContext):
    if str(round(eval(primer[0]), 1)) == message.text:
        await message.answer("Правильно!!!!")
        count_right.append("1")
    else:
        await message.answer("Неправильно!!!!")
        count_wrong.append("1")
    b = prime()
    await message.answer(f'{b} =')
    await igrobot.task.set()
    count.append("1")
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)