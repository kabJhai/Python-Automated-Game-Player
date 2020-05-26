import cv2.cv2
import numpy as np
from PIL import ImageGrab
import win32gui #To access the Windows GUI
import win32api #To get api of the elements
import win32con
import time
import imutils

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
#Resize the window
win32gui.MoveWindow(gameHandle, 0, 0,788,498, True)
kernelOpen = np.ones((3,3))
kernelClose = np.ones((12,12))
#Get the extact position of the window
isFirst = True
firstX = 0
#Set the game window to forground
win32gui.SetForegroundWindow(gameHandle)
#Reload the game
win32api.SendMessage(gameHandle, win32con.WM_KEYDOWN, win32con.VK_F5)
win32api.SendMessage(gameHandle, win32con.WM_KEYUP, win32con.VK_F5)
time.sleep(1)
win32api.SendMessage(gameHandle, win32con.WM_KEYDOWN, win32con.VK_SPACE)
win32api.SendMessage(gameHandle, win32con.WM_KEYUP, win32con.VK_SPACE)
time.sleep(4)

while True:
    position = win32gui.GetWindowRect(gameHandle)
    x,y,w,h = position
    #Take screenshot
    screenshot = ImageGrab.grab(bbox=(x,y,w-200,h)) #give the location to take screenshot from
    #Convert the screenshot to numpy array
    
    screenshot_main = np.array(screenshot)
    #Convert from RGB to BGR for CV2
    screenshot_array = cv2.cvtColor(screenshot_main,cv2.COLOR_RGB2HSV)
    screenshot_array2 = cv2.cvtColor(screenshot_main,cv2.COLOR_RGB2BGR)
    #To get the color of the images for masking
    low = np.array([0,0,166])
    high = np.array([0,0,172])
    mask = cv2.inRange(screenshot_array,low,high)
    #To hide noise
    maskOpen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    contours, h = cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    xs = dict()
    for i in range(len(contours)):
        x,y,w,h = cv2.boundingRect(contours[i])
        if isFirst:
            dinoWidth = x+w
            dinoY = y
            isFirst = False
        if x+w == dinoWidth:
            cv2.rectangle(screenshot_array2,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(screenshot_array2,"Dino",(x,y+h+20),cv2.FONT_HERSHEY_COMPLEX,1,(233,244,255))
        elif(len(contours)>1):
                xs[i] = [x,y]
                cv2.rectangle(screenshot_array2,(x,y),(x+w,y+h),(0,0,255),4)
                cv2.putText(screenshot_array2,str(h),(x,y+h+20),cv2.FONT_HERSHEY_COMPLEX,1,(233,244,255))
    for i in xs.values():
        if((i[0] <= dinoWidth+110) and((dinoY < i[1]) or (((dinoY - i[1])<=8)and((dinoY - i[1])>=0)))):
                win32api.SendMessage(gameHandle, win32con.WM_KEYDOWN, win32con.VK_SPACE)
                win32api.SendMessage(gameHandle, win32con.WM_KEYUP, win32con.VK_SPACE)
                print(i[1],dinoY)    
        elif((i[0] <= dinoWidth+110) and(((i[1]-dinoY)<0))):
                print("Bird",i[1],dinoY)
                win32api.SendMessage(gameHandle, win32con.WM_KEYDOWN, win32con.VK_DOWN)
                time.sleep(0.4)
                win32api.SendMessage(gameHandle, win32con.WM_KEYUP, win32con.VK_DOWN)
    #cv2.WINDOW_NORMAL makes the output window resizealbe
    cv2.namedWindow('Screen', cv2.WINDOW_NORMAL)
 
    #resize the window according to the screen resolution
    cv2.resizeWindow('Screen', 480, 240)
    #Show the image
    cv2.imshow("Screen",screenshot_array2)
    #Wait for 25 milisecond to take another
    key = cv2.waitKey(1)

    #Break when 'A' is pressed on the keybo ard
    if key == 65:
        break

cv2.destroyAllWindows()