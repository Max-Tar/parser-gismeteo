# -*- coding: utf-8 -*-
from datetime import datetime
import cv2

from config import BACKGROUND_COLOR, COLOR_WHITE


def input_data_range():
    """Получение начальной и конечной даты временного диапазона."""

    while True:
        while True:
            text_input = input('Введите начальную дату диапазона в формате 30-05-2022\n')
            try:
                data_begin = datetime.strptime(text_input, '%d-%m-%Y').date()
                break
            except ValueError:
                print('Неверный формат даты!')

        while True:
            text_input = input('Введите начальную дату диапазона в формате 30-05-2022\n')
            try:
                data_end = datetime.strptime(text_input, '%d-%m-%Y').date()
                break
            except ValueError:
                print('Неверный формат даты!')
        if data_end >= data_begin:
            break
        else:
            print('Дата окончания диапазона должна быть после даты начала диапазона, повтори ввод.')

    return data_begin, data_end


def print_weather(weather_data):
    """Вывод на консоль прогнозов."""

    print('Прогноз погоды:')
    for record in weather_data:
        if type(record) is str:
            print(record)
        else:
            for day, item in record.items():
                print(f'Прогноз на {day.strftime("%d-%m-%Y")}:')
                print(f'     Температура от {item["temperature min"]} до {item["temperature max"]},')
                print(f'     Давление от {item["pressure min"]} мм.рт.ст. до {item["pressure max"]} мм.рт.ст.,')
                print(f'     {item["name weather"]}')
                print(f'     Ветер {item["wind direction"]}, скорость {item["wind speed"]} м/с.')


def view_image(image, name_of_window):
    """Вывод карточек."""

    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def formula_lines(y_formula, x_formula, height_formula, width_formula):
    """Расчет для градиента background карточек."""

    angle = 2
    if y_formula < height_formula // 2:
        x_curve = round((height_formula // 2 - y_formula + 30) * angle)
    else:
        x_curve = round((y_formula - height_formula // 2 + 30) * angle)
    if x_formula <= x_curve:
        alpha_formula = 1
    else:
        alpha_formula = 1 - (x_formula - x_curve) / (width_formula - x_curve)
    return alpha_formula


def background_drawing(name, height, width, widget):
    """Создание background карточек."""

    color_background = BACKGROUND_COLOR[widget]
    for x in range(0, width):
        for y in range(0, height):
            alpha = formula_lines(y_formula=y, x_formula=x, height_formula=height, width_formula=width)
            b_color = round((COLOR_WHITE[0] - color_background[0]) * alpha + color_background[0])
            g_color = round((COLOR_WHITE[1] - color_background[1]) * alpha + color_background[1])
            r_color = round((COLOR_WHITE[2] - color_background[2]) * alpha + color_background[2])
            cv2.circle(name, (x, y), 1, (b_color, g_color, r_color), 1)
