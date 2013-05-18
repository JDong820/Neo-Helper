from Neo2 import *


icmC = (0,0,0), (0,0,0)
icmStart = [(0.75, 0.42)]
icmend = [(0.25, 0.70)]
icmRestart = [(0.5, 0.58)]
icmZone = 1, 375.0/569
waitPos = 150./525, 535./570
status = [[],[],[],[],[],[],[]]
cPos = 200./525, 421./567

xGridSize = 0
yGridSize = 0

def setGame():
    setScreenSize()
    findGame2(icmC[0], 150)
    xGridSize = int(getGameDim()[0]/9.0)
    yGridSize = int(getGameDim()[0]/9.0)    
    print "Found game at:", getGamePos()

def play(n=3):
    global waitPos
    global xGridSize
    global yGridSize
    for i in range(n):
        print "Starting game..."
        traversePath(icmStart, 0.1, True, getGamePos()[0])
        while 1:##
            while fuzzyMatch(getColor(waitPos), (0, 48, 99), 40):
                wait(0.3, 0)
            pressKey('space', 1, 0, 0.8)
            wait(0.2, 0)##
            c = getColor(cPos)
            while fuzzyMatch(getColor(waitPos), (0, 48, 99), 40):
                print c
                pos = evaluator(updateArray(c))
                clickRel(int(pos*xGridSize+xGridSize/2), 0.1)
            print 'done'
            wait(1, 0)
        print "Submitting score..."
        traversePath(ffSend, getGamePos()[0], True, 0.2)
        #TODO: improve restarting mech
        time.sleep(0.5)
        if i != n-1:
            traversePath(ffRestart, 0.2, True, getGamePos()[0])

def updateArray(color):
    global status
    #print color
    #color = (255, 102, 153)
    j = 0
    yLim = int(getGameDim()[1]*icmZone[1])
    #0,0,0,0,0,0,0,0,0]
    xstep = int(getGameDim()[0]/9.0)
    ystep = int(yLim/7.0)
    for y in range(ystep, yLim, ystep):
        row = []
        for x in range(xstep/2, getGameDim()[0], xstep):
            #clickRel((x, y), 1)
            if findColor(color, 80, True, (1,1) ,
                         ((x-1,y-ystep), (x+1,y)),
                         getGamePos()[0]) != (-1, -1):
                row.append(1)
                continue
            else:
                row.append(0)
                continue
        status[j] = row
        j += 1
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
                print currLen, i, j
                if currLen == len(arr):
                    return i, j-currLen
                elif currLen > maxLen:
                    point = i, j-currLen
                    maxLen = currLen
                currLen = 0
        if currLen == len(arr):
            return i, j-currLen+1
        elif currLen > maxLen:
            point = i, j-currLen
            maxLen = currLen
        currLen = 0
    return point
            

                
            
