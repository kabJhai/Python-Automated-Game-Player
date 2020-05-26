import cv2.cv2
import numpy as np
from PIL import ImageGrab
import win32gui #To access the Windows GUI
import win32api #To get api of the elements
import win32con
import time
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
else:
    print('Window not available')
    exit(-1)
#Set the game window to forground
win32gui.SetForegroundWindow(gameHandle)
#Get the extact position of the window
while True:
    position = win32gui.GetWindowRect(gameHandle)

    #Press the space key on the keyboard
    win32api.SendMessage(gameHandle, win32con.WM_KEYDOWN, win32con.VK_SPACE)
    win32api.SendMessage(gameHandle, win32con.WM_KEYUP, win32con.VK_SPACE)

    #Take screenshot
    screenshot = ImageGrab.grab(bbox=position) #give the location to take screenshot from
    #Convert the screenshot to numpy array
    screenshot_array = np.array(screenshot)
    #Convert from RGB to BGR for CV2
    screenshot_array = cv2.cvtColor(screenshot_array,cv2.COLOR_RGB2BGR)
    #Show the image
    cv2.imshow("Screen",screenshot_array)
    #Wait for 25 milisecond to take another
    key = cv2.waitKey(25)

    #Break when 'A' is pressed on the keybo ard
    if key == 65:
        break

cv2.destroyAllWindows()