from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

load_dotenv(dotenv_path=r"Путь к .env")
storage = MemoryStorage()
bot_token = os.getenv('TOKEN')
bot = Bot(token=bot_token) 
dp = Dispatcher(bot=bot, storage=storage)
greeting = "Добро пожаловать! Я бот по распознаванию текста на картинке. Пришли мне картинку и я выведу тебе текст, написанный на ней."
download_url = f'https://api.telegram.org/bot{bot_token}/getFile?file_id='
path_to_file_url = f"https://api.telegram.org/file/bot{bot_token}/"
dict_config = {
    'Документ': '--oem 3 --psm 6',
    'Номер телефона': '--oem 3 --psm 12 -c tessedit_char_whitelist=0123456789()-',
    'Номер машины': '--oem 3 --psm 12',
    'Однородный блок текста на картинке': '--oem 3 --psm 6',
    'Текст в произвольных местах': '--oem 3 --psm 11',
    'Рукописный текст': None
}
lang_dict = {
    'Русский': ['rus'],
    'Английский': ['eng'],
    'Русский и Английский': ['en', 'ru']
}

class PhotoStatesGroup(StatesGroup):
    photo = State()
    type_photo = State()
    lang = State()

