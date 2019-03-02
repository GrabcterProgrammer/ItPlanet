#Импортируем библиотеки
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time


white_led = 21 #пин ленты
key = 20 #пин кнопки

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(white_led, GPIO.OUT)
GPIO.setup(key, GPIO.IN)
GPIO.output(white_led, GPIO.LOW)

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')# Файл с характеристиками определения лица

cap = cv2.VideoCapture(0)#Запись видео
cap.set(3,640) # ширина
cap.set(4,480) # высота

# анализ лица и зажигания свет. ленты
def analyz():
    for (x,y,w,h) in faces:
        GPIO.output(white_led, GPIO.HIGH)

def main():
    global white_led, key, cap, faces
    while True:
        ret, img = cap.read() #Чтение видео
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Настройка распознования лица
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
            ,
            minSize=(20, 20),
        )

        GPIO.output(white_led, GPIO.LOW)#

        #Проверка на нажатие кнопки. Если кнопка нажата, то выходим из цикла иначе запустить анализ лица
        if GPIO.input(key) == True:
            #print("key down")
            GPIO.output(white_led, GPIO.LOW)
            break
        else:
            analyz()

main()#Запуск основы проекта
#Проверка на возращение на определение лица
while True:
    time.sleep(1)
    if GPIO.input(key) == True:
        #print("yes")
        main()
