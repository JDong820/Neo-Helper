from NeoAid import *
import time
import random

ffC = (179, 213, 218), (91, 135, 173)

ffStart = [(0.7613, 0.6809), (0.8642, 0.0355)]
ffSend = [(0.7613, 0.6809)]
ffRestart = [(0.7510, 0.5248)]

def play(n=3, mode='farm'):
    global ffC
    time.sleep(1)
    print ('It starts...')
    setScreenSize()
    print 'Screen size:', screenSize
    findGame(ffC[0], ffC[1])
    print 'Found game at:', getGamePos()
    for i in range(n):
        print 'Starting game...'
        traversePath(ffStart, getGamePos()[0], True, 0.2)
        print 'Submitting score...'
        traversePath(ffSend, getGamePos()[0], True, 0.2)
        time.sleep(0.5)
        reX = int(ffRestart[0][0]*getGameDim()[1]+getGamePos()[0][0])
        reY = int(ffRestart[0][1]*getGameDim()[0]+getGamePos()[0][1])
        while getColor((255, 255, 255), True, 0.05, (1,1),
                       ((reX-5, reY-5),
                        (reX+5, reY+5)), 10)[0] == -1:
            print 'Waiting for submission...'
        if i != n-1:
            print 'Restarting game...'
            time.sleep(random.gauss(1, 0.3))
            traversePath(ffRestart, getGamePos()[0], True, 0.2)
            
    


 


