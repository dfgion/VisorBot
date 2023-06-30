from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

type_kb = ReplyKeyboardMarkup(resize_keyboard=True, 
                              one_time_keyboard=True, 
                              row_width=2).insert(KeyboardButton('Документ')).add(KeyboardButton('Номер телефона')).add(KeyboardButton('Номер машины')).insert(KeyboardButton('Рукописный текст')).add(KeyboardButton('Однородный блок текста на картинке')).add(KeyboardButton('Текст в произвольных местах'))
lang_kb = ReplyKeyboardMarkup(resize_keyboard=True, 
                              one_time_keyboard=True, 
                              row_width=2).add(KeyboardButton('Русский')).insert(KeyboardButton('Английский')).add(KeyboardButton('Русский и Английский'))
