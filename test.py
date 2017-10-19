# -*- coding: utf-8 -*-
"""

@author: Saurav Kanchan

"""
import cv2
import pyautogui as pt
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput


W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

handCascade = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
video_capture = cv2.VideoCapture(0)

direction = ""

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    hands = handCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    cv2.line(frame,(0,150),(2000,150),(255,0,0),5)
    cv2.line(frame,(0,300),(2000,300),(255,0,0),5)

    for (x, y, w, h) in hands:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        value = (35, 35)

        blurred = cv2.GaussianBlur(gray[y:y+h, x:x+w], value, 0)

        # thresholdin: Otsu's Binarization method
        _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # show thresholded image

        image, contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        cnt = contours[0]
        M = cv2.moments(cnt)
        try:
            cv2.line(frame, (0, y+h//2), (2000, y+h//2), (0, 255, 0), 5)
            if y+h//2<150:
                direction = "Up"
                PressKey(0x39)
                ReleaseKey(0x39)

            elif y+h//2>300:
                direction = "Down"
                pt.press("down")
            else:
                direction=""


        except:
            pass

    # Display the resulting frame

    cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 0, 255), 3)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()









# import numpy as np
# from PIL import ImageGrab
# import cv2
# import pyautogui as pt
# while(True):
#     printscreen_pil =  ImageGrab.grab(bbox=(0,40,800,640))
#     # printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8')\
#     # .reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))
#     cv2.imshow('window',np.array(printscreen_pil))
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()
#         break


# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html


# if __name__ == '__main__':
#     for i in range(100):
#         key = 0xd0
#         PressKey(key)
#         ReleaseKey(key)