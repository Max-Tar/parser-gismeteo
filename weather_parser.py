# -*- coding: utf-8 -*-
import re
from datetime import date, timedelta
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from config import URL_METEO, HEADERS_METEO


def max_temp_search(tag):
    """Поиск максимальной температуры"""
    if hasattr(tag, 'attrs') and 'class' in tag.attrs:
        if tag.attrs['class'] == ['unit', 'unit_temperature_c']:
            if tag.parent.attrs['class'] == ['maxt']:
                return True
    return False


def min_temp_search(tag):
    """Поиск минимальной температуры"""
    if hasattr(tag, 'attrs') and 'class' in tag.attrs:
        if tag.attrs['class'] == ['unit', 'unit_temperature_c']:
            if tag.parent.attrs['class'] == ['mint']:
                return True
    return False


def max_pressure_search(tag):
    """Поиск максимального давления"""
    if hasattr(tag, 'attrs') and 'class' in tag.attrs:
        if tag.attrs['class'] == ['unit', 'unit_pressure_mm_hg_atm']:
            if tag.parent.attrs['class'] == ['maxt']:
                return True
    return False


def min_pressure_search(tag):
    """Поиск минимального давления"""
    if hasattr(tag, 'attrs') and 'class' in tag.attrs:
        if tag.attrs['class'] == ['unit', 'unit_pressure_mm_hg_atm']:
            if tag.parent.attrs['class'] == ['mint']:
                return True
    return False


def wind_search(tag):
    """Поиск скорости ветра"""
    if hasattr(tag, 'attrs') and 'class' in tag.attrs:
        if tag.attrs['class'] == ['wind-unit', 'unit', 'unit_wind_m_s']:
            if tag.parent.parent.parent.parent.attrs['class'] == ['widget-wrap', 'widget-menu-wrap']:
                return True
    elif tag.text == '—':
        if tag.parent.parent.parent.parent.attrs['class'] == ['widget-wrap', 'widget-menu-wrap']:
            return True
    else:
        return False


def name_widget(text):
    """Поиск характеристики погоды"""
    widget = {'cloud.jpg': ['небольш', ], 'sun.jpg': [r'ясн', r'солн', ], 'snow.jpg': [r'снег', ],
              'rain.jpg': [r'дожд', ], }
    text = text.lower()
    for file, weather_re in widget.items():
        if any(re.search(word_re, text) for word_re in weather_re):
            return file
    else:
        return 'cloud.jpg'


class WeatherMaker:
    """Класс парсера сайта gismeteo.ru"""

    def __init__(self, url=URL_METEO, headers=None):
        if headers is None:
            headers = HEADERS_METEO
        self.url = url
        self.headers = headers

    WIND_DIRECTION = {'В': 'восточный', 'З': 'западный', 'С': 'северный', 'Ю': 'южный', 'СЗ': 'северо-западный',
                      'СВ': 'северо-восточный', 'ЮЗ': 'юго-западный', 'ЮВ': 'юго-восточный', }

    def run(self):
        """Основной метод"""

        response = requests.get(url=self.url, headers=self.headers)
        result = []
        today = date.today()
        one_day = timedelta(days=1)

        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            widget_meteo = html_doc.find_all('div', class_='weather-icon tooltip')
            max_temp_meteo = html_doc.find_all(max_temp_search)
            min_temp_meteo = html_doc.find_all(min_temp_search)
            max_pressure_meteo = html_doc.find_all(max_pressure_search)
            min_pressure_meteo = html_doc.find_all(min_pressure_search)
            wind = html_doc.find_all(wind_search)
            wind_direction = html_doc.find_all('div', class_='direction')

            date_out = today
            for widget, temp_1, temp_2, wind_m_s, wind_direct, pressure1, pressure2 in zip(widget_meteo, max_temp_meteo,
                                                                                           min_temp_meteo, wind,
                                                                                           wind_direction,
                                                                                           max_pressure_meteo,
                                                                                           min_pressure_meteo, ):
                # замена "странного" минуса и буквы "ё"
                if hex(ord(temp_2.text[0])) == '0x2212':
                    temp2_text = '-' + temp_2.text[1:]
                else:
                    temp2_text = temp_2.text
                if hex(ord(temp_1.text[0])) == '0x2212':
                    temp1_text = '-' + temp_1.text[1:]
                else:
                    temp1_text = temp_1.text
                if hex(ord(wind_m_s.text[0])) == '0x2212':
                    wind_m_s_text = '-' + wind_m_s.text[1:]
                else:
                    wind_m_s_text = wind_m_s.text
                name_weather_text = ''
                for char in widget['data-text']:
                    if hex(ord(char)) == '0x451':
                        name_weather_text += 'e'
                    else:
                        name_weather_text += char

                result.append({date_out: {'temperature max': temp1_text, 'temperature min': temp2_text,
                                          'pressure max': pressure1.text,
                                          'pressure min': pressure2.text,
                                          'name weather': name_weather_text,
                                          'name widget': name_widget(text=widget['data-text']),
                                          'wind speed': wind_m_s_text,
                                          'wind direction': self.WIND_DIRECTION[wind_direct.text], }})
                date_out += one_day

        return result


if __name__ == '__main__':
    weather = WeatherMaker()
    weather_data = weather.run()
    pprint(weather_data)
