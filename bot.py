from service_info import dp, bot, greeting, download_url, path_to_file_url, PhotoStatesGroup, dict_config, lang_dict
import aiohttp
from visor import tess_visor, easy_visor, keras_visor
from aiogram import types, executor
from keyboards import type_kb, lang_kb
from aiogram.dispatcher import FSMContext
import logging
import shutil

async def on_startup(_):
    logging.info('bot was started')

@dp.message_handler(commands = ['start'])
async def command_start(message: types.Message):
    logging.info('User sent a command /start')
    await bot.send_message(chat_id=message.chat.id, text=greeting)
    await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEJO-Jkf5GZ-dCO4T3wGzzFjksgFB_JgwACYAIAAgvNDgNERok1XlXTOS8E')
    await PhotoStatesGroup.photo.set()

@dp.message_handler(content_types=['photo'], state=PhotoStatesGroup.photo)
async def photo_handler(message: types.message, state: FSMContext):
    logging.info('State: Photo ')
    logging.info('The bot received the photo ')
    picture = bytearray()
    logging.info('Aiohttp request is processing')
    async with aiohttp.ClientSession() as session:
        resp = await session.get(download_url+message.photo[2].file_id)
        resp = await resp.json(encoding='UTF-8')
        async with session.get(path_to_file_url+resp['result']['file_path']) as responce:
            async for chunk in responce.content.iter_chunked(64*1024):
                picture += chunk     
    logging.info('Photo has been downloaded from Telegram Server')
    async with state.proxy() as data:
        data['photo'] = picture
        logging.info('Photo saved in MemoryStorage')
    await message.answer('Какой тип больше подходит данному тексту?', reply_markup=type_kb)
    await PhotoStatesGroup.next()

@dp.message_handler(state=PhotoStatesGroup.type_photo)
async def type_picture(message: types.message, state: FSMContext):
    logging.info('State: Mode for OCR')
    logging.info('Mode for OCR was recieved')
    if message.text in list(dict_config.keys()):
        async with state.proxy() as data:
            logging.info('Mode saved in MemoryStorage')
            data['type'] = message.text 
    else:
        await message.answer('Некорретный ответ, выбрал стандартный режим')
        logging.warning('Was set a standart Mode. User sent uncorrect mode')
        async with state.proxy() as data:
            data['type'] = 'Однородный блок текста на картинке'
    logging.info('Mode saved in MemoryStorage')
    await message.answer('Какой язык на картинке?', reply_markup=lang_kb)
    await PhotoStatesGroup.lang.set()

@dp.message_handler(state=PhotoStatesGroup.lang)
async def type_picture(message: types.message, state: FSMContext):
    logging.info('State: Language')
    logging.info('Language was recieved')
    if message.text in list(lang_dict.keys()):
        async with state.proxy() as data:
            data['lang'] = message.text  
    else:
        await message.answer('Некорректный ответ. Выбран английский язык по умолчанию')
        async with state.proxy() as data:
            data['lang'] = 'Английский'     
        logging.info('Uncorrect language. Was set a stardart language')
    logging.info('Language was saved in MemoryStorage')   
    await message.answer('Обработка... Это может занять минуту.')
    logging.info("Was start a function 'Visor'. Data was sent to processing") 
    text = tess_visor(image=data['photo'], type_picture=data['type'], language=data['lang'])
    await message.answer(f" {text[0]}\n Pytessart\n Time: {text[1]}")
    text = easy_visor(image=data['photo'], type_picture=data['type'], language=data['lang'])
    await message.answer(f" {text[0]}\n EasyOCR\n Time: {text[1]}")
    text = keras_visor()
    await message.answer(f" {text[0]}\n KerasOCR\n Time: {text[1]}")
    shutil.rmtree('images')
    await message.answer('Ожидаю следующую картинку!')
    await PhotoStatesGroup.photo.set()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="bot.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    executor.start_polling(dispatcher=dp, skip_updates = True, on_startup=on_startup)