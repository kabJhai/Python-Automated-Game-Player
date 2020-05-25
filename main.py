import cv2
import numpy as np
from PIL import ImageGrab
import win32gui

#Take screenshot
screenshot = ImageGrab.grab(bbox=(0 ,0 , 500, 500)) #give the location to take screenshot from
screenshot.show()