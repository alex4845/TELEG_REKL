import time
import asyncio
import io
from aiogram.types import ParseMode
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from reklama_data import *

storage = MemoryStorage()
bot = Bot('5917858144:AAHRyeAdLmAfuDsuZAAv5jUXs4U9cG3sa34')
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item3 = types.KeyboardButton("Список каналов для мониторинга")
    item2 = types.KeyboardButton("Получить 10 последних креативов")
    item4 = types.KeyboardButton("Добавить канал")
    item5 = types.KeyboardButton("Удалить канал")
    item6 = types.KeyboardButton("Сколько креативов в базе")
    markup.add(item3, item6, item2)
    await message.answer('Выбор действия:', reply_markup=markup)

class FSMchannel(StatesGroup):
    name_channel = State()

class FSMchannel_d(StatesGroup):
    del_channel = State()

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=None)
async def answer(message: types.Message):
    mess1 = message.text
    if mess1 == "Получить 10 последних креативов":
        r = await read_from_base(10)
        for post in r:
            try:
                screenshot_data, screenshot_name = post[-1], str(post[0]) + '.png'
                screenshot_entity = types.InputFile(io.BytesIO(screenshot_data), filename=screenshot_name)
                await message.answer_photo(photo=screenshot_entity, caption=post[1] + post[2], parse_mode=ParseMode.HTML)
            except:
                continue
    if mess1 == "Список каналов для мониторинга":
        r = await read_from_base_channels()
        l, c = "", 0
        for i in r:
            c += 1
            l = l + f'{i}\n'
            if c == 50:
                await message.answer(l)
                c = 0
                l = ""
        await message.answer(l)

    if mess1 == "Добавить канал":
        await FSMchannel.name_channel.set()
        await message.answer('Введите название канала (Пример: kinopoisk):')
    if mess1 == "Удалить канал":
        await FSMchannel_d.del_channel.set()
        await message.answer('Введите номер канала, который хотите удвлить:')
    if mess1 == "Сколько креативов в базе":
        last = await read_from_base(1)
        await message.answer(f'Всего:  {last[0][0]}')

@dp.message_handler(content_types=['text'], state=FSMchannel.name_channel)
async def add_channel(message: types.Message, state: FSMContext):
        res_chek = await chek_channel(message.text)
        if res_chek:
            await message.answer("Такой канал есть в списке")
        else:
            r = await write_to_base_channels(message.text)
            await message.answer(r)
        await state.finish()

@dp.message_handler(content_types=['text'], state=FSMchannel_d.del_channel)
async def del_channel(message: types.Message, state: FSMContext):
        res = await del_channel(message.text)
        await message.answer(res)
        await state.finish()

async def interval(d):
    # t_n = datetime.now()
    # current_time = datetime.now().replace(hour=19, minute=10, second=0)
    # current_time1 = datetime.now().replace(hour=19, minute=15, second=0)
    #if t_n > current_time and t_n < current_time1:
        r = await read_from_base(d)
        c = 0
        for post in r:
            c += 1
            screenshot_data, screenshot_name = post[-1], str(post[0]) + '.png'
            screenshot_entity = types.InputFile(io.BytesIO(screenshot_data), filename=screenshot_name)
            await bot.send_photo(chat_id=-1002018831317, photo=screenshot_entity, caption=post[1] + post[2],
                                       parse_mode=ParseMode.HTML)
            if c == 20:
                time.sleep(62)
                c = 0

# async def scheduled(wait_for):
#     while True:
#         await asyncio.sleep(wait_for)
#         await interval()

#loop = asyncio.get_event_loop()
#loop.create_task(scheduled(200))
executor.start_polling(dp, skip_updates=True)
