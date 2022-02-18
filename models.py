# -*- coding: utf-8 -*-
from datetime import date

import peewee
from playhouse.db_url import connect

from config_db import WEATHER_CONFIG, DB_CONFIG

database_proxy = peewee.DatabaseProxy()


class Weather(peewee.Model):
    day_weather = peewee.DateField()
    temperature_max = peewee.CharField()
    temperature_min = peewee.CharField()
    pressure_max = peewee.CharField()
    pressure_min = peewee.CharField()
    name_weather = peewee.CharField()
    name_widget = peewee.CharField()
    wind_speed = peewee.CharField()
    wind_direction = peewee.CharField()

    class Meta:
        database = database_proxy


if WEATHER_CONFIG['DEBUG']:
    database = peewee.SqliteDatabase('local.db')
elif WEATHER_CONFIG['TESTING']:
    database = peewee.SqliteDatabase(':memory:')
else:
    database = connect(**DB_CONFIG)

database_proxy.initialize(database)

if __name__ == '__main__':
    date_search = date.today()
    record = Weather.get(Weather.day_weather == date_search)
    print(record.name_weather)
