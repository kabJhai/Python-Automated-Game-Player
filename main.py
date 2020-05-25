import cv2
import numpy as np
from PIL import ImageGrab
import win32gui

#Take screenshot
screenshot = ImageGrab.grab()
screenshot.show()