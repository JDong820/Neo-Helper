import win32api
from PIL import ImageGrab
import time

def monitorMouse(delay = 0.2):
    while 1:
        time.sleep(delay)
        pos = win32api.GetCursorPos()
        img = ImageGrab.grab()
        rgb_im = img.convert('RGB')
        print rgb_im.getpixel(pos)

monitorMouse()
