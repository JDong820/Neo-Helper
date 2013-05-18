from NeoAid import *
import time

tugC = (121, 83, 138), (234, 206, 109)
tugStart = [(0.1657, 0.9424), (0.3304, 0.5132), (0.81, 0.50)]
tugSend = [(0.7, 0.943)]
tugRestart = [(0.5, 0.34)]

def play(n=3, mode='farm'):
    global tugC
    
    print ("It starts...")
    setScreenSize()
    print "Screen size:", screenSize
    findGame(tugC[0], tugC[1])
    print "Found game at:", getGamePos()
    print 'Game mode:', mode
    for i in range(n):
        print "Starting game..."
        traversePath(tugStart, getGamePos()[0], True, 0.2)
        time.sleep(0.5)
        if mode == 'hiscore' or mode == 'farm':
            for i in range(7):
                while getColor(tugC[0], True, 0, (1,1),
                               (getGamePos()[0],
                                (getGamePos()[0][0]+2,
                                 getGamePos()[0][1]+2)), 0)[0] == -1:
                    time.sleep(0.1)
                pressKey('A',10000)
                time.sleep(4)
                pressKey('A',1)
            print 'Submitting score...'
            traversePath(tugSend, getGamePos()[0], True, 0.2)
            reX = int(tugRestart[0][0]*getGameDim()[1]+getGamePos()[0][0])
            reY = int(tugRestart[0][1]*getGameDim()[0]+getGamePos()[0][1])
            while getColor((255, 255, 255), True, 0.05, (1,1),
                           ((reX-5, reY-5),
                           (reX+5, reY+5)), 10)[0] == -1:
                print 'Waiting for submission...'
            if n-1 > 0:
                print 'Restarting game...'
                traversePath(tugRestart, getGamePos()[0], True, 0.2)

                
