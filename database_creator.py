# -*- coding: utf-8 -*-
import peewee
from models import Weather

database = peewee.SqliteDatabase('external_data/weather.db')
database.create_tables([Weather])
