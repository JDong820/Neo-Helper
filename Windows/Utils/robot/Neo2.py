import win32api, win32con
from PIL import ImageGrab, Image
import time
import random
import visualizer
import re

gamePos = []
gameLen = 0
gameHeight = 0
screenSize = 0

#output functions
def pressKey(key = 'A', n = 10000,
             delayPre = 0, delayDown = 0.1):
    '''
    Press the alphanumeric key n times.
    '''
    if len(re.findall('[a-zA-Z0-9]', str(key))) == 1:
        key = str(key)
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

def typeStr(msg, delayPre=0.05, delayDown=0.05):
    '''
    Type the string with the given delays.
    '''
    for char in range(msg.upper()):
        pressKey(char, 1, delayPre, delayDown)

def clickAbs(absPos, downTime=0):
    '''
    Click on the screen with an (x,y) input.
    '''
    print absPos
    win32api.SetCursorPos(absPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(downTime)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def clickRel(relPos, downTime):
    '''
    Click in the game with a (x,y) input.
    '''
    global gamePos
    if relPos[0] > gamePos[1][0] or relPos[1] > gamePos[1][1]:
        print 'Error. Position out of bounds.'
        return
    clickAbs((int(gamePos[0][0]+relPos[0]), int(gamePos[0][1]+relPos[1])),
              downTime)

def clickRatio(ratioPos, downTime):
    '''
    Click in the game with a ratio input.
    '''
    global gameLen
    global gameHeight
    clickRel((ratioPos[0]*gameLen, ratioPos[1]*gameHeight), downTime)

def traversePath(points, downTime = 0.01, click=False, ref=(0,0)):
    '''
    Traverse the given path.
    Defaults to clicking in the game.
    Set click to True to click at each point on the path.
    '''
    pos = (0,0)
    for p in points:
        if p[0] < 1 and p[1] < 1:
            pos = int(p[0]*gameLen)+ref[0], int(p[1]*gameHeight)+ref[1]
        elif p[0] >= 1 and p[1] >= 1:
            pos = p[0]+ref[0], p[1]+ref[1]
        else:
            print 'ERROR: Point format not detected.'
            break
        if click:
            clickAbs(pos, downTime)
            time.sleep(downTime)
        else:
            win32api.SetCursorPos(pos)

def wait(avg=1, dev=0.3):
    if dev != 0:
        time.sleep(random.gauss(avg, dev))
    else:
        time.sleep(avg)

#Color Analysis
def fuzzyMatch(c1, c2, fuzz, mode='basic'):
    '''
    Perform fuzzy color match with rgb difference fuzz.
    Use 'basic' mode for unshared tolerence.
    Use 'conservative' for shared tolerence.
    '''
    if mode == 'basic':
        for i in range(len(c1)):
            if c1[i]+fuzz < c2[i] or c1[i]-fuzz > c2[i]:
                return False
        return True
    elif mode == 'conservative':
        for i in range(len(c1)):
            #abs
            fuzz -= ((c1[i]-c2[i])**2)**0.5
        if fuzz >= 0:
            return True
        else:
            return False

def matches(rgb_im, fuzz, region, relPos, forward=True):
    '''
    Match an image against a point on the screen.
    '''
    if forward:
        for x_im in range(rgb_im.size[0]):
            for y_im in range(rgb_im.size[1]):
                if rgb_im.getpixel((x_im, y_im)) !=\
                   region.getpixel((x_im+relPos[0], y_im+relPos[1])):
                    return False
    else:
        for x_im in reversed(range(rgb_im.size[0])):
            for y_im in reversed(range(rgb_im.size[1])):
                if rgb_im.getpixel((x_im, y_im)) !=\
                   region.getpixel((x_im+relPos[0], y_im+relPos[1])):
                    return False
    return True
                
    
def findImg(rgb_im, fuzz=0, forward=True,
            region=[(0,0), (1366, 768)], ref=(0,0)):
    '''
    Find the first match on the screen for
    the given image in the specified region.
    '''
    box = (region[0][0]+ref[0], region[0][1]+ref[1],
           region[1][0]+ref[0], region[1][1]+ref[1])
    search = ImageGrab.grab().crop(box)
    if forward:#Search from the top left corner.
        findPx = rgb_im.getpixel((0,0))
        for i in range(search.size[0]):
            for j in range(search.size[1]):
                #i,j = relative
                #x,y = absolute
                x = i+box[0]
                y = j+box[1]
                #
                #win32api.SetCursorPos((x+1, y+1))
                #time.sleep(0.003)
                if matches(rgb_im, fuzz, search, (i,j), True):
                    return (x,y)
    else: #Search from the bottom right corner.
        findPx = rgb_im.getpixel((rgb_im.size[0]-1, rgb_im.size[1]-1))
        for i in reversed(range(search.size[0])):
            for j in reversed(range(search.size[1])):
                x = i+box[0]
                y = j+box[1]
                if matches(rgb_im, fuzz, search, (i,j), True):
                    return (x,y)
    return (-1,-1)

def getScreen():
    return ImageGrab.grab()

def getColor((x,y), rel=(0,0), im = False):
    if x<1:
        x = int(x*getGameDim()[0])
    if y<1:
        y = int(y*getGameDim()[1])
    pos = rel[0]+getGamePos()[0][0]+x, rel[1]+getGamePos()[0][1]+y
    #win32api.SetCursorPos(pos)
    #time.sleep(0.2)
    if im:
        return im.getpixel(pos)
    else:
        return ImageGrab.grab().getpixel(pos)

def findColor(rgb, fuzz=0, forward=True, size=(1,1),
              region=((0,0), (1366,768)), ref=(0,0)):
    '''
    Find a region of color of a given size.
    '''
    im = Image.new('RGB', size, rgb)
    return findImg(im, fuzz, forward, region, ref)

##def quickFindColor(rgb, forward=True):
##    screen = ImageGrab.grab()
##    if forward:
##        for x in range(screen.size[0]):
##            for y in range(screen.size[1]):
##                if screen.getpixel((x,y)) == rgb:
##                    return (x,y)
##    else:
##        for x in reversed(range(screen.size[0])):
##            for y in reversed(range(screen.size[1])):
##                if screen.getpixel((x,y)) == rgb:
##                    return (x,y)

def findThick(color, fuzz, rgb_im, im_pos,
              sweeps, thickness, errorOver, errorUnder, mode):
    '''
    Return start and endpoints of homogeneous color lines.
    mode = 'x' for vertical sweeps
    mode = 'y' for horizontal sweeps
    rgb_im = 0 for all screen
    sweeps = 0 for sweeping every pixel
    thickness = 0 for all results
    '''
    segments = []
    if rgb_im == 0:
        rgb_im = ImageGrab.grab()
    if mode == 'x':
        print 'vertical scan'
        step = int(rgb_im.size[0]/(sweeps+1))
        if step < 1 or sweeps == 0:
            step = 1
        for x in range(0, rgb_im.size[0], step):
            currLen = 0
            for y in range(0, rgb_im.size[1]):
                win32api.SetCursorPos((x+im_pos[0]+1, y+im_pos[1]+1))
                if fuzzyMatch(rgb_im.getpixel((x,y)), color, fuzz):
                    currLen += 1
                else:
                    if currLen == 0:
                        continue
                    elif thickness == 0:
                        segments.append(((x,y-currLen), (x,y)))
                        currLen = 0
                        continue
                    elif (thickness-errorUnder > currLen) or\
                       (thickness+errorOver < currLen):
                        currLen = 0
                        continue
                    else:
                        segments.append(((x,y-currLen), (x,y)))
                        count = 0
                        continue
    if mode == 'y':
        print 'horizontal scan'
        step = int(rgb_im.size[1]/(sweeps+1))
        if step < 1 or sweeps == 0:
            step = 1
        for y in range(0, rgb_im.size[1], step):
            currLen = 0
            for x in range(0, rgb_im.size[0]):
                win32api.SetCursorPos((x+im_pos[0]+1, y+im_pos[1]+1))
                if fuzzyMatch(rgb_im.getpixel((x,y)), color, fuzz):
                    currLen += 1
                else:
                    if currLen == 0:
                        continue
                    elif thickness == 0:
                        segments.append(((x-currLen,y), (x,y)))
                        currLen = 0
                        continue
                    elif (thickness-errorUnder > currLen) or\
                       (thickness+errorOver < currLen):
                        currLen = 0
                        continue
                    else:
                        segments.append(((x-currLen,y), (x,y)))
                        count = 0
                        continue
    return segments

#screen and game
def findGame(color1, color2):
    '''
    Locates the game based on images of
    the upper left and bottom right corners.
    '''
    global gameLen
    global gameHeight
    global gamePos
    global screenSize
    
    gamePos = (findColor(color1, 0, True, (1,1)),
               findColor(color2, 0, False, (1,1)))
    gameLen = gamePos[1][0]-gamePos[0][0]
    gameHeight = gamePos[1][1]-gamePos[0][1]

def findGame2(color, res=200, mode='x'):
    global gamePos
    global gameLen
    global gameHeight
    
    lines = findThick(color, 0, 0, (0,0), res, 0, 0, 0, mode)
    d = []
    for l in lines:
        val = dist(l[0], l[1])
        if val > 1:
            d.append(val)
    dAvg = avg(d)*1
    begin = 0
    end = 0
    for i in range(len(lines)):
        if dist(lines[i][0], lines[i][1]) > dAvg:
            begin = lines[i][0]
            break
    for i in reversed(range(len(lines))):
        if dist(lines[i][0], lines[i][1]) > dAvg:
            end = lines[i][1]
            break
##    print begin, end
##    print lines
##    import grapher
##    grapher.setData('screen', lines, [], [begin, end], 0.8)
##    grapher.main()    
    gamePos = (begin, end)
    gameLen = gamePos[1][0]-gamePos[0][0]
    gameHeight = gamePos[1][1]-gamePos[0][1]

def setScreenSize():
    global screenSize
    screenSize = ImageGrab.grab().size

def getGamePos():
    return gamePos

def getGameDim():
    return gameLen, gameHeight

#analytical geometry
def cornersToBox(corners):
    return (corners[0][0], corners[0][1], corners[1][0], corners[1][1])

def avg(l):
    a = 0
    for d in l:
        a += d
    return a/float(len(l))

def dist(p1, p2):
    if len(p1) != len(p2):
        print "Error: wrong dimensions."
        return False
    t = 0
    for i in range(len(p1)):
        t += (p1[i]-p2[i])**2
    return t**0.5

def removeDuplicates(points):
    new = []
    s = set()
    for p in points:
        if not p in s:
            s.add(p)
            new.append(p)
    return new

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

def midpoint(points):
    xTotal = 0
    yTotal = 0
    for p in points:
        xTotal += p[0]
        yTotal += p[1]
    return (xTotal/len(points), yTotal/len(points))

def addMidpoints(points, newD=0):
    '''
    Add the midpoints of the given points for each consecutive pair.
    '''
    i = 0
    while i < len(points):
        points.insert(i+1, midpoint(points[i:i+2]))
        i += 2
    return points

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

#TODO
def elminateLoops(path):
    for i in range(len(path)):
        for p2 in new:
            print 'hi'

#DEBUG
def showIm(im):
    im.show()




##a = Image.new('RGB', (5,5), 'yellow')
##a = a.putpixel(tuple((1,1)), 'black')
##a.show()
