# -*- coding: utf-8 -*-
from datetime import timedelta

from models import Weather
from utils import input_data_range
from weather_parser import WeatherMaker


class DatabaseUpdater:
    """Класс работы с базой данных погоды."""

    def __init__(self):
        self.weather_maker = WeatherMaker()
        self.db_weather = Weather

    def upload_dates_parser(self):
        """Метод выбора данных для загрузки и их передача на загрузку."""

        weather_data = self.weather_maker.run()
        print('\nС сайта gismeteo.ru загружена информация о погоде в городе Жуковский на даты:')
        for record in weather_data:
            for key in record.keys():
                print(key.strftime("%d-%m-%Y"))
        print('\nВведите начальную и конечную дату диапазона дат для загрузки в базу данных')
        begin_range, end_range = input_data_range()
        weather_for_update = []
        for day in weather_data:
            for key in day.keys():
                if begin_range <= key <= end_range:
                    weather_for_update.append(day)

        self.update_db_weather(weather_update=weather_for_update)

    def update_db_weather(self, weather_update):
        """Метод загрузки и/или обновления данных в базе."""

        for data_weather in weather_update:
            for key in data_weather.keys():
                try:
                    record = self.db_weather.get(self.db_weather.day_weather == key)
                    record.temperature_max = data_weather[key]['temperature max']
                    record.temperature_min = data_weather[key]['temperature min']
                    record.pressure_max = data_weather[key]['pressure max']
                    record.pressure_min = data_weather[key]['pressure min']
                    record.name_weather = data_weather[key]['name weather']
                    record.name_widget = data_weather[key]['name widget']
                    record.wind_speed = data_weather[key]['wind speed']
                    record.wind_direction = data_weather[key]['wind direction']
                    record.save()

                except Weather.DoesNotExist:
                    record = self.db_weather(day_weather=key,
                                             temperature_max=data_weather[key]['temperature max'],
                                             temperature_min=data_weather[key]['temperature min'],
                                             pressure_max=data_weather[key]['pressure max'],
                                             pressure_min=data_weather[key]['pressure min'],
                                             name_weather=data_weather[key]['name weather'],
                                             name_widget=data_weather[key]['name widget'],
                                             wind_speed=data_weather[key]['wind speed'],
                                             wind_direction=data_weather[key]['wind direction'])
                    record.save()

    def search_weather_day(self, data_search):
        """Метод получения одной записи из базы данных."""

        try:
            note = self.db_weather.get(Weather.day_weather == data_search)
            result = {'temperature max': note.temperature_max, 'temperature min': note.temperature_min,
                      'pressure max': note.pressure_max, 'pressure min': note.pressure_min,
                      'name weather': note.name_weather, 'name widget': note.name_widget,
                      'wind speed': note.wind_speed, 'wind direction': note.wind_direction}
            return result
        except Weather.DoesNotExist:
            return False

    def search_weather_several(self, begin, end):
        """Метод получения записей из базы данных за диапазон дат."""
        one_day = timedelta(days=1)
        day_for_search = begin
        total_result = []

        while day_for_search <= end:
            result = self.search_weather_day(data_search=day_for_search)
            if result:
                total_result.append({day_for_search: result})
            else:
                total_result.append(f'На дату {day_for_search.strftime("%d-%m-%Y")} данных нет.')
            day_for_search += one_day

        return total_result

    def first_last_record(self):
        """Метод вывода на консоль начальной о конечной записи в базе данных."""
        first_record_query = self.db_weather.select().limit(1).order_by(self.db_weather.id.asc())
        for item in first_record_query.dicts().execute():
            print(f'Дата первой записи в базе данных: {item["day_weather"].strftime("%d-%m-%Y")}')
        last_record_query = self.db_weather.select().limit(1).order_by(self.db_weather.id.desc())
        for item in last_record_query.dicts().execute():
            print(f'Дата последней записи в базе данных: {item["day_weather"].strftime("%d-%m-%Y")}')


if __name__ == '__main__':
    weather = DatabaseUpdater()
    weather.upload_dates_parser()
