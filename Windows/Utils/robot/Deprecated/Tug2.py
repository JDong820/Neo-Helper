from Neo2 import *

tugC = (121, 83, 138), (234, 206, 109)
tugStart = [(0.1657, 0.9424), (0.3304, 0.5132), (0.81, 0.50)]
tugSend = [(0.7, 0.943)]
tugRestart = [(0.5, 0.34)]

def play(n=3, mode='farm'):
    global tugC
    
    print ("It starts...")
    setScreenSize()
    findGame(tugC[0], tugC[1])
    print "Found game at:", getGamePos()
    print 'Game mode:', mode
    for i in range(n):
        print "Starting game..."
        traversePath(tugStart, 0.2, True, getGamePos()[0])
        wait(1, 0)
        if mode == mode:
            for i in range(7):
                while 1:
                    if findColor(tugC[0], 0, True, (1,1),
                                 ((0,0),(2,2)), getGamePos()[0]) != (-1,-1):
                        print 'ready.'
                        break
                    wait(0.2, 0)
                    clickRel((0.5, 0.5), 0.1)
                    print 'waiting...'
                print 'win?'
                pressKey('A', 1000, 0.001, 0.001)
                print 'winning.'
                time.sleep(4)
                pressKey('A',1)
            print 'Submitting score...'
            traversePath(tugSend, 0.2, True, getGamePos()[0])
            reX = int(tugRestart[0][0]*getGameDim()[0])
            reY = int(tugRestart[0][1]*getGameDim()[1])
            while findColor((255, 255, 255), 0, True, (1,1),
                            ((reX-5, reY-5), (reX+5, reY+5)),
                            getGamePos()[0]) == (-1,-1):
                print 'Waiting for submission...'
            if n-1 > 0:
                print 'Restarting game...'
                traversePath(tugRestart, 0.2, True, getGamePos()[0])

                
