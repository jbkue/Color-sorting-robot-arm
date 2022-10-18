import sys
import time
from returnThreading import ReturnValueThread
import cv2
import serial
import numpy as np
from threading import Thread
from queue import Queue

ser = serial.Serial(port="/dev/ttyACM1", baudrate=115200, timeout=5)
ser.flush()
cam = cv2.VideoCapture(0)


def get_color_values():
    _, frame = cam.read()
    cv2.imshow("frame", frame)
    roi = frame[213:626, 160:320]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    cv2.imshow("ROI", roi)
    upper_blue = np.array([128, 255, 255])
    upper_red = np.array([9, 255, 255])
    lower_blue = np.array([90, 50, 70])
    lower_red = np.array([0, 50, 70])
    blue_mask = cv2.inRange(roi, lower_blue, upper_blue)
    red_mask = cv2.inRange(roi, lower_red, upper_red)
    cv2.imshow("red", red_mask)
    cv2.imshow("blue", blue_mask)
    blue = blue_mask
    red = red_mask
    blue = np.mean(blue)
    red = np.mean(red)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
    blue, red = int(blue), int(red)
    blue, red = str(blue), str(red)
    blue, red = blue.encode('utf-8'), red.encode('utf-8')
    return blue, red


def send_arduino(blue, red):
    ser.write(blue + b" " + red + b"\n")
    time.sleep(15)
    print(int(blue), int(red))
    sys.exit()


while True:
    colors = Thread(target=get_color_values, args=())
    ReturnValueThread(colors)
    print(int(blue_val), int(red_val))
