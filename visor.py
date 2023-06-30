from PIL import Image
import pytesseract
import time
import io
import os
import secrets
from service_info import dict_config, lang_dict
import easyocr
import keras_ocr
from glob import glob
import logging

def main_visor(image: bytearray, type_picture: str, language: str):
    logging.basicConfig(level=logging.INFO, filename="bot.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    if not os.path.exists('images'):
        os.mkdir('images')
        logging.info("Was created service dicrectory for processing")
    filename = secrets.token_hex(8)   
    cmd_lang = lang_dict[language]                                                                                                                                                                                                          
    service_img = Image.open(io.BytesIO(image)) # создание Image объекта
    logging.info('Image was translated to bytestr')
    service_img = service_img.convert('L')
    logging.info('Image was converted to GRAY')
    service_img.save(f'images/{filename}.png', format='PNG') # Сохранение Image объекта
    logging.info('Image was saved in dicrectory')
    return {'mode': type_picture, 'filename': filename, 'language': cmd_lang}

def tess_visor(image: bytearray, type_picture: str, language: str):
    data = main_visor(image=image, type_picture=type_picture, language=language)
    logging.info('Tesseract. Processing... 10%')
    if len(data['language'])>1:
        formatted_lang = 'eng'
    else:
        formatted_lang = data['language'][0]
    bytestr = bytearray() # создание переменной для хранения изображения в байтстроке
    with open(f"images/{data['filename']}.png", 'rb') as f:
        for chunk in f:
            bytestr+= chunk
    logging.info('Tesseract. Processing... 25%')
    service_img = Image.open(io.BytesIO(bytestr))
    pytesseract.pytesseract.tesseract_cmd = r"Путь к Tesseract" # Находится в архиве Tesseract.zip (tesseract.exe)
    logging.info('Tesseract. Processing... 50%')
    start = time.time()
    text = pytesseract.image_to_string(service_img, lang=formatted_lang, config=dict_config[data['mode']])
    logging.info('Tesseract. Processing... 75%')
    end = time.time()
    time_tess = end-start
    logging.info('Tesseract. Processing... 100%')
    os.remove(f"images/{data['filename']}.png")
    return (text, time_tess)

def easy_visor(image: bytearray, type_picture: str, language: str):
    data = main_visor(image, type_picture, language)
    logging.info('EasyOCR. Processing... 10%')
    correct_languages = [lang[0:2] for lang in data['language']]
    reader = easyocr.Reader(lang_list=correct_languages, gpu=True)
    logging.info('EasyOCR. Processing... 25%')
    start = time.time()
    text = reader.readtext(f"images/{data['filename']}.png", paragraph=True, detail=0, batch_size=1)
    logging.info('EasyOCR. Processing... 50%')
    end = time.time()
    time_easy = end-start
    logging.info('EasyOCR. Processing... 100%')
    return (''.join(text), time_easy)

def keras_visor():
    logging.info('KerasOCR. Processing... 10%')
    pipeline = keras_ocr.pipeline.Pipeline()
    logging.info('KerasOCR. Processing... 30%')
    start = time.time()
    images = [keras_ocr.tools.read(img) for img in glob('images/*')]
    logging.info('KerasOCR. Processing... 50%')
    results = pipeline.recognize(images)
    end = time.time()
    time_keras = end-start
    logging.info('KerasOCR. Processing... 75%')
    result = ''
    for word in results[0][1:]:
        result += f' {word[0]}'
    logging.info('KerasOCR. Processing... 100%')
    return (result, time_keras)


