# Тг-бот, распознающий текст на картинке
Данный бот работает на основе библиотек с обученными нейронными сетями.
1. Pytesseract
2. EasyOCR
3. KerasOCR 

В проекте присутствует файл bot.py. В этом файле прописала логика работы самого бота в среде Telegram с помощью библиотеки aiogram.
Вторым основным файлом является visor.py. В данном файле прописана работа библиотек с компьютерным зрением.

Для работы с pytesseract требуется установка самого Tesseract.
Скачать его можно тут: https://tesseract-ocr.github.io/tessdoc/Downloads.html

После установки Tesseract нужно будет указать в коде файла visor.py путь в файлу tesseract.exe. (Отмечено комментарием)

Также вам требуется получить token бота. 
Указать его нужно будет либо в файле .env, а затем в файле service_info.py (Отмечено комментарием) указать путь к .env