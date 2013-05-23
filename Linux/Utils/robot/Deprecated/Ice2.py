from Neo2 import *


icmC = (0,0,0), (0,0,0)

icmStart = [(0.75, 0.42)]
icmEnd = [(0.25, 0.70)]
icmRestart = [(0.5, 0.58)]

icmZone = 1, 339./605
waitPos = 175./525, 532./570
cPos = 200./525, 421./567

verifyArr = []

xGridSize = 0
yGridSize = 0

def setGame():
    global yGridLim
    global xGridSize
    global yGridSize
    setScreenSize()
    findGame2(icmC[0], 150)
    yGridLim = int(getGameDim()[1]*icmZone[1])
    xGridSize = int(getGameDim()[0]/9.0)
    yGridSize = int(yGridLim/6.0)
    print 'Found game at:', getGamePos()
    print 'Ice cream dim:', xGridSize, yGridSize
    print 'yLim:', yGridLim

def play(n=3):
    global status
    global waitPos
    global xGridSize
    global yGridSize
    setGame()
    for i in range(n):
        print 'It starts...'
        clickRatio(icmStart[0], 0)
        wait(4)
        while 1:##
            print 'NEW LEVEL'
            pressKey('space', 1, 1, 0.01)
            #c = getColor(cPos)
            #print 'Color:', c
            clickRatio((0.8,0.8), 0)
            scanInit()
            while fuzzyMatch (getColor(waitPos), (0, 48, 99), 0):
                print 'updating...'
                updateArray()
                print 'evaluating...'
                pos = evaluator(status)
##                if isinstance(pos, int):
##                    print 'pos:', pos
##                    break
                clickRel((int(pos[0]*xGridSize+xGridSize/2), int(pos[1]*yGridSize+yGridSize/2)), 0)
                #wait(0.1)
            print 'Waiting...'
            wait(3)
        print 'Submitting score...'
        traversePath(ffSend, getGamePos()[0], True, 0.2)
        #TODO: improve restarting mech
        wait(0.5)
        if i != n-1:
            traversePath(ffRestart, 0.2, True, getGamePos()[0])
##def updateArray(color):
##    global status
##    global yGridLim
##    global xGridSize
##    global yGridSize
##    j = 0
##    yLim = int(getGameDim()[1]*icmZone[1])
##    xstep = int(getGameDim()[0]/9.0)
##    ystep = int(yLim/7.0)
##    for y in range(yGridSize, yGridLim, yGridSize):
##        row = []
##        for x in range(xGridSize/2, getGameDim()[0], xGridSize):
##            #clickRel((x, y), 1)
##            if findColor(color, 100, True, (1,1) ,
##                         ((x-1,y-yGridSize), (x,y)),
##                         getGamePos()[0]) != (-1, -1):
##                row.append(1)
##                continue
##            else:
##                row.append(0)
##                continue
##        status[j] = row
##        j += 1
##    return status
def updateArray():
    global verifyArr
    global status
    temp = -1
    im = getScreen()
    status = []
    for row in verifyArr:
        newRow = []
        for xy, color in row:
            if temp == -1:
                temp = (getColor(xy, (0,0), im) != color)
            elif temp == 1:
                newRow.append(1)
                temp = -1
            elif temp == 0:
                newRow.append(int(getColor(xy, (0,0), im) != color))
                temp = -1
        status.append(newRow)
    return status
                
def evaluator(arr):
    maxLen = 0
    currLen = 0
    point = 0
    for i in range(len(arr[0])):
        for j in range(len(arr)):
            if arr[j][i] == 0:
                currLen += 1
            else:
                #print currLen, i, j
                if currLen == len(arr):
                    return i, j-currLen   +1
                elif currLen > maxLen:
                    point = i, j-currLen  +1
                    maxLen = currLen
                currLen = 0
        if currLen == len(arr):
            return i, j-currLen+1         +1
        elif currLen > maxLen:
            point = i, j-currLen          +1
            maxLen = currLen
        currLen = 0
    return point
            
def scanInit():
    global verifyArr
    global yGridLim
    global xGridSize
    global yGridSize
    im = getScreen()
    #showIm(im)
    verifyArr = []
    for y in range(0, yGridLim-1, yGridSize):
        row = []
        for x in range(0, getGameDim()[0]-1, xGridSize):
            xi, yi = x+(xGridSize/2), y+6
            row.append(((xi,yi), getColor((xi,yi), (0,0), im)))
            xi, yi = x+(xGridSize/2), y-6+yGridSize
            row.append(((xi,yi), getColor((xi,yi), (0,0), im)))
        verifyArr.append(row)
    return verifyArr
            
