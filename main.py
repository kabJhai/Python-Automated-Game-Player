import cv2
import numpy as np
from PIL import ImageGrab
import win32gui

toplist = []
windowList = []
def enum_win(windowHandle, result):
    windowText = win32gui.GetWindowText(windowHandle)
    windowList.append((windowHandle,windowText))

#Get the list of open windows and p
win32gui.EnumWindows(enum_win, toplist)

#To get the handle of the game
gameHandle = 0
for (handle,text) in windowList:
    if 'chrome://dino/' in text:
        gameHandle = handle
if gameHandle != 0:
    pass

#Get the extact position of the window
position = win32gui.GetWindowRect(gameHandle)
print(position)
#Take screenshot
#screenshot = ImageGrab.grab(bbox=(0 ,0 , 500, 500)) #give the location to take screenshot from
#screenshot.show()