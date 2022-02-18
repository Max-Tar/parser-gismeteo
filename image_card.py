# -*- coding: utf-8 -*-
import cv2

from config import COLOR_TEXT, CARD_TEXT_POSITION, CARD_TEXT_AFTER, CARD_TEXT_BEFORE
from utils import view_image, background_drawing
from weather_parser import WeatherMaker


class ImageMaker:
    """Класс рисования карточек."""

    def __init__(self, text, url='external_data/', template='probe.jpg'):
        self.text = text
        self.url = url
        self.template = template
        self.card = None

    def run(self):
        """Основной метод."""

        self.card = cv2.imread(filename=self.url + self.template)
        height, width, _ = self.card.shape
        font = cv2.FONT_HERSHEY_COMPLEX
        if type(self.text) is not str:
            for key in self.text.keys():
                widget_bg = self.text[key]['name widget']
                background_drawing(name=self.card, height=height, width=width, widget=widget_bg)

                widget = cv2.imread(filename=self.url + 'weather_img/' + widget_bg)
                roi = self.card[10:110, 10:110]
                widget_gray = cv2.cvtColor(widget, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(widget_gray, 10, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)
                card_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
                widget_fg = cv2.bitwise_and(widget, widget, mask=mask)
                added = cv2.add(card_bg, widget_fg)
                self.card[10:110, 10:110] = added

        if type(self.text) is not str:
            for key in self.text.keys():
                text_header1 = 'Прогноз погоды в г. Жуковский'
                self.card = cv2.putText(img=self.card, text=text_header1, org=(130, 50), fontFace=font, fontScale=0.6,
                                        color=COLOR_TEXT, thickness=1)
                text_header2 = 'на ' + key.strftime("%d-%m-%Y")
                self.card = cv2.putText(img=self.card, text=text_header2, org=(205, 90), fontFace=font, fontScale=0.6,
                                        color=COLOR_TEXT, thickness=1)
                for value, position in CARD_TEXT_POSITION.items():
                    text_for_position = CARD_TEXT_BEFORE[value] + self.text[key][value] + CARD_TEXT_AFTER[
                        value]
                    self.card = cv2.putText(img=self.card, text=text_for_position, org=CARD_TEXT_POSITION[value],
                                            fontFace=font, fontScale=0.5, color=COLOR_TEXT, thickness=1)
        else:
            self.card = cv2.putText(img=self.card, text=self.text, org=(130, 50), fontFace=font, fontScale=0.4,
                                    color=COLOR_TEXT, thickness=1)
        view_image(self.card, 'Card')


if __name__ == '__main__':
    weather = WeatherMaker()
    weather_data = weather.run()
    for weather_for_day in weather_data:
        card_image = ImageMaker(text=weather_for_day)
        card_image.run()
