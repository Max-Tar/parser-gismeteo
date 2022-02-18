# -*- coding: utf-8 -*-

URL_METEO = 'https://www.gismeteo.ru/weather-zhukovsky-11329/10-days/'
HEADERS_METEO = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

COLOR_BLUE = [255, 77, 0]
COLOR_BLUE_DIFF = [0, 178, 255]
COLOR_LIGHT_BLUE = (238, 238, 175)
COLOR_YELLOW = (0, 255, 255)
COLOR_GREY = (128, 128, 128)
COLOR_WHITE = (255, 255, 255)
COLOR_TEXT = (0, 0, 0)
CARD_TEXT_POSITION = {'temperature max': (230, 165), 'temperature min': (50, 165), 'pressure max': (200, 190),
                      'pressure min': (50, 190),
                      'name weather': (50, 140), 'wind speed': (50, 240), 'wind direction': (50, 215), }
CARD_TEXT_BEFORE = {'temperature max': ' до ', 'temperature min': 'Температура от ', 'pressure max': ' до ',
                    'pressure min': 'Давление от ', 'name weather': '', 'wind speed': 'Скорость ветра ',
                    'wind direction': 'Ветер ', }
CARD_TEXT_AFTER = {'temperature max': ' гр.С', 'temperature min': '', 'pressure max': ' мм.рт.ст. ',
                   'pressure min': '', 'name weather': '', 'wind speed': ' м/с ', 'wind direction': '', }
BACKGROUND_COLOR = {'cloud.jpg': COLOR_GREY, 'sun.jpg': COLOR_YELLOW, 'snow.jpg': COLOR_LIGHT_BLUE,
                    'rain.jpg': COLOR_BLUE, }

TEXT_FOR_HELP = 'Введите одну из команд для работы скрипта: Команда "add" запускает процесс обновления и ' \
                'добавления прогнозов погоды в базу данных. Команда "get" запускает процесс получения прогнозов ' \
                'погоды из базы данных и вывод их на консоль. Команда "card" запускает процесс  получения ' \
                'прогнозов погоды из базы данных и вывод их в виде карточек'


