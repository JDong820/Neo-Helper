import win32api, win32con
import time
import random

#Keyboard out
def outKey(key = 'A', n = 1,
             delayPre = 0, delayDown = 0.1):
    '''
    Press the key n times.
    '''
    key = str(key)
    if len(re.findall('[a-zA-Z0-9]', str(key))) == 1:
        if not re.match('[0-9]', key):
            key = key.upper()
        for i in range(n):
            time.sleep(delayPre)
            win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
            time.sleep(delayDown)
            win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_KEYUP, 0)
    else:
        if key == 'space':
            key = win32con.VK_SPACE
        elif key == 'up':
            key = win32con.VK_UP
        elif key == 'down':
            key = win32con.VK_DOWN
        elif key == 'left':
            key = win32con.VK_LEFT
        elif key == 'right':
            key = win32con.VK_RIGHT
        for i in range(n):
            time.sleep(delayPre)
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
            time.sleep(delayDown)
            win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
def outStr(msg, delayPre=0.05, delayDown=0.05):
    '''
    Type the string with the given delays.
    '''
    for c in range(msg):
        outKey(c, 1, delayPre, delayDown)

#Mouseclick out
def clickAbs(absPos, downTime=0):
    '''
    Click on the computer screen.
    '''
    print absPos
    win32api.SetCursorPos(absPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(downTime)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
def clickRel(relPos, downTime):
    '''
    Click in the game using game-relative coordinates.
    '''
    global gamePos
    if relPos[0] > gamePos[1][0] or relPos[1] > gamePos[1][1]:
        print 'Error. Position out of bounds.'
        return
    clickAbs((int(gamePos[0][0]+relPos[0]), int(gamePos[0][1]+relPos[1])),
              downTime)
def clickRatio(ratioPos, downTime):
    '''
    Click in the game with a xy-ratio input.
    '''
    global gameLen
    global gameHeight
    clickRel((ratioPos[0]*gameLen, ratioPos[1]*gameHeight), downTime)
def traversePath(points, downTime = 0.01, click=False, ref=(0,0)):
    '''
    Traverse the given game path.
    Do not mix ratio and relative point formats.
    Set click to True to click at each point on the path.
    '''
    if 0 < p[0] < 1 and 0 < p[1] < 1:
        ratioMode = True
        relMode = False
    elif p[0] >= 1 and p[1] >= 1:
        ratioMode = False
        relMode = True
    for p in points:
        if ratioMode:
            pos = int(p[0]*gameLen)+ref[0], int(p[1]*gameHeight)+ref[1]
        elif gameRelMode:
            pos = p[0]+ref[0], p[1]+ref[1]
        else:
            print 'ERROR: Point format not detected.'
            break
        if click:
            clickAbs(pos, downTime)
        else:
            win32api.SetCursorPos(pos)
