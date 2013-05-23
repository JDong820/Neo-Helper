import win32api, win32con
from PIL import ImageGrab
import time

gamePos = []
gameLen = 0
gameHeight = 0
screenSize = 0

#Output functions    
def pressKey(key = 'A', times = 10000, delay = 0, downTime = 0.1, reclickTime = 0.1):
    time.sleep(delay)
    for i in range(times):
        win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(downTime)
        win32api.keybd_event(ord(key), 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(reclickTime)

def typeStr(msg, downTime = 0.1, reclickTime = 0.1):
    for c in range(msg.upper()):
        pressKey(c, 1, 0, downTime, reclickTime)

def clickRatio(ratioPos):
    global gameLen
    global gameHeight
    clickRel((ratioPos[0]*gameLen, ratioPos[1]*gameHeight))

def clickRel(relPos, delay=0):
    global gamePos
    if relPos[0] > gamePos[1][0] or relPos[1] > gamePos[1][1]:
        print 'Error. Position out of bounds.'
        return
    win32api.SetCursorPos((int(gamePos[0][0]+relPos[0]), int(gamePos[0][1]+relPos[1])))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def clickAbs(absPos, downTime=0):
    win32api.SetCursorPos(absPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(downTime)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def traversePath(points, rel=True, click=False, delay=0):
    global gamePos
    print gamePos
    ref = (0,0)
    if rel == True:
        ref = gamePos
    for p in points:
        if p[0] < 1 and p[1] < 1:
            win32api.SetCursorPos((int(p[0]*gameLen)+ref[0], int(p[1]*gameHeight)+ref[1]))
        elif p[0] >= 1 and p[1] >= 1 :
            win32api.SetCursorPos((p[0]+ref[0], p[1]+ref[1]))
        else:
            print 'Error. Path point format not detected.'
        time.sleep(delay)
        if click:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

#Screen analysis
def findGame(color1, color2):
    global gameLen
    global gameHeight
    global gamePos
    global screenSize
    
    gamePos = [getColor(color1, True, 0, (1,1), ((0,0), screenSize), 0),
               getColor(color2, False, 0, (1,1), ((0,0), screenSize), 0)]
    gameLen = gamePos[1][0]-gamePos[0][0]
    gameHeight = gamePos[1][1]-gamePos[0][1]

def setScreenSize():
    global screenSize
    screenSize = ImageGrab.grab().size



#Calculations
def interpolate(p1, p2, d=1):
    partitions = (dist(p1, p2)/d)-1
    if partitions != int(partitions):
        partitions = int(partitions)+1
    partitions = int(partitions)
    if partitions < 1:
        print "Adjacent points given."
        return [p1, p2]
    partitionLen = dist(p1, p2)/(partitions+1)
    dirIncrement = (((p2[0]-p1[0])/float(dist(p1, p2))), ((p2[1]-p1[1])/float(dist(p1, p2))))
    points = [p1]
    for i in range(partitions):
        points.append(((points[-1][0]+dirIncrement[0]*partitionLen), (points[-1][1]+dirIncrement[1]*partitionLen)))
    points.append(p2)
    for i in range(len(points)):
        points[i] = (int(points[i][0]), int(points[i][1]))
    return points

def removeDuplicates(points):
    new = []
    for p in points:
        if not p in new:
            new.append(p)
    return new

def addMidpoints(points, newD=0):
    '''
    Add the midpoints of the given points for each consecutive pair.
    '''
    i = 0
    while i < len(points):
        points.insert(i+1, midpoint(points[i:i+2]))
        i += 2
    return points

def midpoint(points):
    xTotal = 0
    yTotal = 0
    for p in points:
        xTotal += p[0]
        yTotal += p[1]
    return (xTotal/len(points), yTotal/len(points))

def dist(p1, p2):
    if len(p1) != len(p2):
        print "Error: wrong dimensions."
        return False
    t = 0
    for i in range(len(p1)):
        t += (p1[i]-p2[i])**2
    return t**0.5

def doesIntersect(segment1, segment2):
    if segment1[0][0] == segment1[1][0]:
        print 'need isBetween method'
    elif segment2[0][0] == segment2[1][0]:
        print 'I am derp.'
    else:
        slope1 = float(segment1[1][1]-segment1[0][1])/(segment1[1][0]-segment1[0][0])
        slope2 = float(segment2[1][1]-segment2[0][1])/(segment2[1][0]-segment2[0][0])
        y1 = segment1[0][1]-segment1[0][0]*slope1
        y2 = segment2[0][1]-segment2[0][0]*slope2
        solX = ((segment1[0][1]-segment2[0][1])-(y1-y2))/(slope1-slope2)
        if segment1[0][0] < solX and solX < segment1[1][0] and segment2[0][0] < solX and solX < segment2[1][0]:
            return True
    return False

def elminateLoops(path):
    for i in range(len(path)):
        for p2 in new:
            print 'derp'
def avgPath(path):
    newPath = [path[0]]
    for i in range(len(path)-2):
        estP = midpoint((path[i], path[i+2]))
        newPath.append(midpoint((path[i+1], estP)))
    newPath.append(path[-1])
    return newPath

def closestPoint(initial, points):
    minDist = 90000
    myPoint = 0
    for p in points:
        if dist(initial, p) < minDist:
            minDist = dist(initial, p)
            myPoint = p
            if minDist == 0:
                print "Need to fix code."
    return myPoint

#Accessors
def getGamePos():
    return gamePos

def getGameDim():
    return gameHeight, gameLen


def cornersToBox(corners):
    return (corners[0][0], corners[0][1], corners[1][0], corners[1][1])

#Image analysis
def fuzzyMatch(c1, c2, fuzz):
    for i in range(len(c1)):
        if c1[i]+fuzz < c2[i] or c1[i]-fuzz > c2[i]:
            return False
    return True

def matchesRect(pos, size, rgb, fuzz, rgb_im=0):
    '''
    Warning: this function is slow.
    '''
    if rgb_im == 0:
        print "matchRect() called without image. May cause slowness."
        im = ImageGrab.grab()
        rgb_im = im.convert('RGB')
    #rgb_im = rgb_im.crop(cornersToBox([pos, (pos[0]+size[0], pos[1]+size[1])]))
    for x in range(pos[0], pos[0]+size[0]):
        for y in range(pos[1], pos[1]+size[1]):
            if not fuzzyMatch(rgb, rgb_im.getpixel((x,y)), fuzz):
                return False
    return True
    
def getColor(rgb=(255,255,255), forward=True, delay=0,
             size=(2,2), region=[(0,0), (1366, 768)], fuzz=0):
    im = ImageGrab.grab()
    rgb_im = im.convert('RGB')
    if forward:
        for x in range(region[0][0], region[1][0]):
            for y in range(region[0][1], region[1][1]):
                win32api.SetCursorPos((x-1,y-1))
                time.sleep(delay)
                px = rgb_im.getpixel((x, y))
                if fuzzyMatch(px, rgb, fuzz) and matchesRect((x,y), size, rgb, fuzz, rgb_im):
                        return (x,y)
    else:
        for x in reversed(range(region[0][0], region[1][0])):
            for y in reversed(range(region[0][1], region[1][1])):
                win32api.SetCursorPos((x-1,y-1))
                time.sleep(delay)
                px = rgb_im.getpixel((x, y))
                if fuzzyMatch(px, rgb, fuzz) and matchesRect((x,y), size, rgb, fuzz, rgb_im):
                    return (x,y)
    return (-1,-1)
    
def findThick(rgb_img, mode='x', sweeps=50,
              color=(0,0,0), thickness=20, error=5, fuzz=1):
    '''
    Return start and endpoints of homogeneous color regions.
    mode = 'x' for vertical sweeps
    mode = 'y' for horizontal sweeps
    '''
    global gamePos
    
    segments = []
    if mode == 'x':
        step = int(rgb_img.size[0]/(sweeps+2))
        if step < 1:
            step = 1
        for x in range(step, rgb_img.size[0], step):
            count = 0
            for y in range(0, rgb_img.size[1]):
                win32api.SetCursorPos((x+gamePos[0][0]-1,y+gamePos[0][1]-1))
                px = rgb_img.getpixel((x,y))
                #time.sleep(0.001)
                if fuzzyMatch(px, color, fuzz):
                    count += 1
                    #time.sleep(0.01)
                else:
                    if count < thickness-error or count > thickness+error:
                        count = 0
                        continue
                    else:
                        segments.append(((x,y-count),(x,y)))
                        #time.sleep(1)
                        count = 0
                        continue
    elif mode == 'y':
        step = int(rgb_img.size[1]/(sweeps+2))
        if step < 1:
            step = 1
        for y in range(step, rgb_img.size[1], step):
            count = 0
            for x in range(0, rgb_img.size[0]):
                win32api.SetCursorPos((x+gamePos[0][0]-1,y+gamePos[0][1]-1))
                px = rgb_img.getpixel((x,y))
                #time.sleep(0.001)
                if fuzzyMatch(px, color, fuzz):
                    count += 1
                    #time.sleep(0.01)
                else:
                    if count < thickness-error or count > thickness+error:
                        count = 0
                        continue
                    else:
                        segments.append(((x-count,y),(x,y)))
                        #time.sleep(1)
                        count = 0
                        continue
    return segments

def getCircle(pos, size, rgb, fuzz = 0):
    print 'derp'


    
