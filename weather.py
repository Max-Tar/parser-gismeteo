# -*- coding: utf-8 -*-
import argparse

from config import TEXT_FOR_HELP
from database_work import DatabaseUpdater
from image_card import ImageMaker
from utils import input_data_range, print_weather


def get_args():
    """Метод получения аргумента командной строки."""

    parser = argparse.ArgumentParser(description='Script for viewing weather forecasts in the city of Zhukovsky')
    parser.add_argument('command', type=str, help=TEXT_FOR_HELP)
    return parser.parse_args()


class UserConsole:
    """Класс обработки пользовательского запроса."""

    def __init__(self, dbase):
        self.argument = get_args()
        self.dbase = dbase

    def run(self):
        """Основной метод класса."""
        handler = getattr(UserConsole, self.argument.command, None)
        if handler is not None:
            handler(self)
        else:
            print('Команда не распознана, "-h" выведет описание скрипта.')

    def add(self):
        """Метод добавления данных в базу."""
        self.dbase.upload_dates_parser()

    def get(self):
        """Метод получения данных из базы и вывод их на консоль"""
        self.dbase.first_last_record()
        day_begin_get, day_end_get = input_data_range()
        several_days_weather_get = self.dbase.search_weather_several(begin=day_begin_get, end=day_end_get)
        print_weather(several_days_weather_get)

    def card(self):
        """Метод получения данных из базы и вывод их в виде карточек"""
        self.dbase.first_last_record()
        day_begin, day_end = input_data_range()
        several_days_weather = self.dbase.search_weather_several(begin=day_begin, end=day_end)
        for weather_for_day in several_days_weather:
            card_image = ImageMaker(text=weather_for_day)
            card_image.run()


if __name__ == '__main__':
    weather_db = DatabaseUpdater()
    user = UserConsole(weather_db)
    user.run()
