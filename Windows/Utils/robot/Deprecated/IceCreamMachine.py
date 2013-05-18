from NeoAid import *
import time

icmC = (0,0,0), (0,0,0)
icmStart = [(0.75, 0.42)]
icmend = [(0.25, 0.70)]
icmRestart = [(0.5, 0.58)]

def setGame():
    setScreenSize()
    findGame(icmC[0], icmC[1])
    print "Found game at:", getGamePos()

def play(n=3):
    time.sleep(0.2)
    print ("It starts...")
    for i in range(n):
        print "Starting game..."
        traversePath(icmStart, getGamePos()[0], True, 0.2)
        ##
        ##
        print "Submitting score..."
        traversePath(ffSend, getGamePos()[0], True, 0.2)
        #TODO: improve restarting mech
        time.sleep(0.5)
        if i != n-1:
            traversePath(ffRestart, getGamePos()[0], True, 0.2)
            
    


 


