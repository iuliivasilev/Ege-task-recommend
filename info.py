from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import types

import kernel as kl
import plots as pl

TOKEN = '1501680189:AAF17qdgtNHR1O3mNo_VI72ckSUrwY7ThmA'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def select_answer(d_button):
    keyboard = types.InlineKeyboardMarkup();
    for i,v in d_button.items():
    	key = types.InlineKeyboardButton(text=i, callback_data=v); 
    	keyboard.add(key);
    return keyboard

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")

#########################################################
@dp.message_handler() #commands=['help']
async def process_help_command(message: types.Message):
    id_ = message.from_user.id
    main_class.new_user(id_)
    keyboard = select_answer({'Дать номер':'task',#'Рейтинг':'rating',
                              'История номеров':'stories',
                              'Рейтинг':'ratingvis'})
    await bot.send_message(id_, text = 'Возможные действия:', reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == 'rating')
async def callback_worker(callback_query: types.CallbackQuery):
    id_ = callback_query.from_user.id
    await bot.send_message(id_, text = str(main_class.get_rating(id_)))
    
@dp.callback_query_handler(lambda call: call.data == 'stories')
async def callback_worker(callback_query: types.CallbackQuery):
    id_ = callback_query.from_user.id
    await bot.send_message(id_, text = str(main_class.get_stories(id_)))
    
@dp.callback_query_handler(lambda call: call.data == 'ratingvis')
async def callback_worker(callback_query: types.CallbackQuery):
    id_ = callback_query.from_user.id
    rat = list(main_class.get_rating(id_))
    photo = pl.save_plot(rat)
    with open(photo, "rb") as file:
    	data = file.read()
    await bot.send_photo(id_, photo=data)

#########################################################
'''
@dp.message_handler(commands=['rating'])
async def process_help_command(message: types.Message):
    await message.reply(main_class.get_rating(message.from_user.id))
    
@dp.message_handler(commands=['stories'])
async def process_help_command(message: types.Message):
    await message.reply(main_class.get_stories(message.from_user.id))
'''
#########################################################
@dp.callback_query_handler(lambda call: call.data == 'task')
async def get_task(msg: types.CallbackQuery): #Message
    numb_task = main_class.get_task(msg.from_user.id)
    text = 'https://inf-ege.sdamgia.ru/problem?id=' + str(numb_task)
    keyboard = select_answer({'Верно':'yes','Неверно':'no'})
    await bot.send_message(msg.from_user.id, text, reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == 'yes')
async def callback_worker(callback_query: types.CallbackQuery):
    main_class.get_answer(callback_query.from_user.id, True)
    text = "Well done! Напишите любое сообщение, чтобы продолжить!\n"
    await bot.send_message(callback_query.from_user.id, text)

@dp.callback_query_handler(lambda call: call.data == 'no')
async def callback_worker(callback_query: types.CallbackQuery):
    main_class.get_answer(callback_query.from_user.id, False)
    text = "Okeyyy... Напишите любое сообщение, чтобы продолжить!\n"
    await bot.send_message(callback_query.from_user.id, text)
#########################################################
if __name__ == '__main__':
    global main_class
    try:
        main_class = kl.Task_info('./users.xlsx','./tasks.xlsx')
        executor.start_polling(dp, skip_updates=True)
    except:
        print('here')
    main_class = None
