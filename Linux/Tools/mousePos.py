import win32api
import time

def monitorMouse(delay = 0.2):
    while 1:
        time.sleep(delay)
        pos = win32api.GetCursorPos()
        print pos
        
def setMouse(xy):
    win32api.SetCursorPos(xy)

