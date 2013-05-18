from NeoAid import *
import time

domeC1, domeC2 = (22, 26, 36),(228, 228, 230)
fightPos = 0
skipPos = 0
fightC = (255, 254, 0)
grey = (71,71,71)


if __name__ == '__main__':
    print ("It starts...")
    setScreenSize()
    print "Screen size:", screenSize
    findGame(domeC1, domeC2)
    print "Found game at:", getGamePos()
    fightPos = getColor(fightC, True, 0, (1,1), (getGamePos()[0], getGamePos()[1]), 0)
    fightPos = fightPos[0]-2, fightPos[1]-2
    skipPos = getColor(grey, True, 0, (1,1), ((fightPos[0], getGamePos()[0][1]), getGamePos()[1]), 0)
    print "Fighting..."
    count = 0
    while 1:
        if getColor(grey, True, 0, (1,1), (skipPos, (skipPos[0]+2, skipPos[1]+2)), 2)[0] != -1:
            clickAbs(skipPos)
            time.sleep(0.1)
        print count
        count += 1
        if getColor(fightC, True, 0, (1,1), (fightPos, (fightPos[0]+4, fightPos[1]+4)), 2)[0] != -1:
            clickAbs(fightPos)
            time.sleep(0.7)
        time.sleep(0.3)
#TODO: server error refreshing
        
