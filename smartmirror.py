# -*- coding: utf-8 -*-
'''
id Городов России

20 Архангельск
1092 Назрань
37 Астрахань
30 Нальчик
197	Барнаул
47 Нижний Новгород
4 Белгород
65 Новосибирск
77 Благовещенск
66 Омск
191	Брянск
10 Орел
24 Великий Новгород
48 Оренбург
75 Владивосток
49 Пенза
33 Владикавказ
50 Пермь
192	Владимир
25 Псков
38 Волгоград
39 Ростов-на-Дону
21 Вологда
11 Рязань
193	Воронеж
51 Самара
1106 Грозный
2 Санкт-Петербург
54 Екатеринбург
42 Саранск
5 Иваново
12 Смоленск
63 Иркутск
239	Сочи
41 Йошкар-Ола
36 Ставрополь
43 Казань
973	Сургут
22 Калининград
13 Тамбов
64 Кемерово
14 Тверь
7 Кострома
67 Томск
35 Краснодар
15 Тула
62 Красноярск
195	Ульяновск
53 Курган
172	Уфа
8 Курск
76 Хабаровск
9 Липецк
45 Чебоксары
28 Махачкала
56 Челябинск
1 Москва и Московская область
1104 Черкесск
213	Москва
16 	Ярославль
23 	Мурманск
'''

from tkinter import *
import locale
import threading
import time
import requests
import traceback
import feedparser

from PIL import Image, ImageTk
from contextlib import contextmanager
from bs4 import BeautifulSoup

LOCALE_LOCK = threading.Lock()

ui_locale = '' # например 'fr_FR' для французского, '' по умолчанию
date_format = "%b %d, %Y" # проверьте Python Doc для strftime () для
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

@contextmanager
def setlocale(name): #функция доказательства потока для работы с локалью
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # инициализировать метку времени
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # инициализировать день недели
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # инициализировать метку даты
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        global time2
        with setlocale(ui_locale):
            time2 = time.strftime('%H:%M') #часы 24 формат

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # если временная строка изменилась, обновите ее
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # Вазывает себя каждые 200 миллисекунд
            # обновить отображение времени по мере необходимости
            # может использовать> 200 мс, но отображение становится прерывистым
            self.timeLbl.after(200, self.tick)

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg='black')
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica 20'), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica 14'), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    def get_weather(self):
        r = requests.get('https://export.yandex.ru/bar/reginfo.xml?region=76') #Парсим сайт погоды, чтобы поменять регион подставить всместо "76" свой id Города
        soup = BeautifulSoup(r.text, 'lxml') #'Парсим сайт погоды'...
        #Берем температуру
        temperature2 = 'temperature'
        find_temperature = soup.find(temperature2)
        self.temperature = find_temperature.text
        #Место расположения
        location2 = 'title'
        find_location = soup.find(location2)
        self.location = find_location.text
        #Текущая погода
        currently2 = 'weather_type'
        find_currently = soup.find(currently2)
        self.currently = find_currently.text
        #Вывод на экран
        self.temperatureLbl.config(text=self.temperature)
        self.currentlyLbl.config(text=self.currently.upper())
        self.locationLbl.config(text=self.location.upper())

        if self.currently == 'ясно':
            if time2 < '19:30' and time2 > '08:00':
                image = Image.open('img/Sun.png')
                image = image.resize((100, 100), Image.ANTIALIAS)
                image = image.convert('RGB')
                photo = ImageTk.PhotoImage(image)
                self.iconLbl.config(image=photo)
                self.iconLbl.image = photo
            else:
                image = Image.open('img/Moon.png')
                image = image.resize((100, 100), Image.ANTIALIAS)
                image = image.convert('RGB')
                photo = ImageTk.PhotoImage(image)
                self.iconLbl.config(image=photo)
                self.iconLbl.image = photo

        elif self.currently == 'облачно':
            image = Image.open('img/Cloud.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            self.iconLbl.config(image=photo)
            self.iconLbl.image = photo

        elif self.currently == 'переменная облачность' or self.currently == 'облачно с прояснениями':
            if time2 < '19:30' and time2 > '08:00':
                image = Image.open('img/PartlySunny.png')
                image = image.resize((100, 100), Image.ANTIALIAS)
                image = image.convert('RGB')
                photo = ImageTk.PhotoImage(image)
                self.iconLbl.config(image=photo)
                self.iconLbl.image = photo
            else:
                image = Image.open('img/PartlyMoon.png')
                image = image.resize((100, 100), Image.ANTIALIAS)
                image = image.convert('RGB')
                photo = ImageTk.PhotoImage(image)
                self.iconLbl.config(image=photo)
                self.iconLbl.image = photo

        elif self.currently == 'дождь':
            image = Image.open('img/Rain.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            self.iconLbl.config(image=photo)
            self.iconLbl.image = photo

        elif self.currently == 'снег' or self.currently == 'облачно, небольшой снег' or self.currently == 'облачно, снег' :
            image = Image.open('img/Snow.png')
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = image.convert('RGB')
            photo = ImageTk.PhotoImage(image)
            self.iconLbl.config(image=photo)
            self.iconLbl.image = photo

        self.after(1000, self.get_weather)



class News(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'Новости' # Надпись "Новости"
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.newsLbl.pack(side=TOP, anchor=W)
        self.headlinesContainer = Frame(self, bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        try:
            for widget in self.headlinesContainer.winfo_children():
                widget.destroy()
            headlines_url = "https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru"
            feed = feedparser.parse(headlines_url)
            for post in feed.entries[0:5]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)
        except Exception as e:
            traceback.print_exc()
            self.newsLbl = Label(self, text='Отсутсвует подключение к интернету', font=('Helvetica 40'), fg="white", bg="black")
            self.newsLbl.pack(side=TOP, anchor=W)

        self.after(600000, self.get_headlines)


class NewsHeadline(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        image = Image.open("img/Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)


class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # часы
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # погода
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)
        # новости
        self.news = News(self.bottomFrame)
        self.news.pack(side=LEFT, anchor=S, padx=100, pady=60)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
