from NeoAid import *
import visualizer
import time
import win32api
from PIL import ImageGrab

buzzerPx = [(46, 95, 44), (38, 45, 26)]
buzzerMenu = [(0.68, 0.77)]
buzzerLvl = [(0.76, 0.58)]
lineRatio = 0.0259

green = (0, 158, 0)
green2 = (0, 204, 0)
red = (204, 0, 0)
black = (0, 0, 0)

lineWidth = 0
begin = (0.0856793, 0.4888889)
end = (0.9388004, 0.4991452)

def findInit():
    global begin
    v = getColor((0, 180, 0), True, 0, (1,1), getGamePos(), 40)
    if v[0] < 0 and v[1] < 0:
        v = getColor((0, 180, 0), True, 0, (1,1), getGamePos(), 40)
    begin = (v[0]+5, v[1]-3)
    
def findTarget():
    global end
    v = getColor(red, False, 0, (1,1), getGamePos(), 0)
    end = (v[0]-5, v[1])

def getLineWidth():
    global lineWidth
    lineWidth = int(lineRatio*getGameDim()[0])
    return lineWidth

def createWaypoints(tolerence=0.3, passX=40, passY=30):
    global lineWidth
    
    waypoints = []
    rgb_game = ImageGrab.grab(cornersToBox([getGamePos()[0], getGamePos()[1]])).convert('RGB')
    print "Finding vertical waypoints..."
    for s in findThick(rgb_game, 'x', passX, black, lineWidth, int(lineWidth*tolerence), 1):
        waypoints.append(midpoint(s))
    print "Finding horizontal waypoints..."
    for s in findThick(rgb_game, 'y', passY, black, lineWidth, int(lineWidth*tolerence), 1):
        waypoints.append(midpoint(s))
    return waypoints

def sortWaypoints(points):
    global begin
    global end

    points.append((end[0]-getGamePos()[0][0], end[1]-getGamePos()[0][1]))
    path = []
    p = (begin[0]-getGamePos()[0][0], begin[1]-getGamePos()[0][1])
    while len(points) > 0:
        p = closestPoint(p, points)
        path.append(p)
        points.remove(p)
    return path

def pruneWaypoints(points):
    '''
    Calculate average distance between consecutive points and
    eliminate points above average.
    '''
    e = (end[0]-getGamePos()[0][0], end[1]-getGamePos()[0][1])
    for i in range(len(points)):
        if points[i] == e:
            break
    return points[:i]
    
##    for x in range(getGamePos()[0][0], getGamePos()[1][0], resolution):
##        for y in range(getGamePos()[0][1], getGamePos()[1][1]):
##            if matchesRect((x,y), (1,lineWidth-1), black, 10, rgb_im):
##                win32api.SetCursorPos((x,y))
##                time.sleep(0.5)
##    print "Finding horizontal waypoints..."
###        t = getColor(black, True, 0.01, (1,lineWidth-1), [(x, getGamePos()[0][1]), (x+1, getGamePos()[1][1])], 0
##    for y in range(getGamePos()[0][1], getGamePos()[1][1], resolution):
##        print "Finding point for y =", y
##        t = getColor(black, True, 0.01, (1,lineWidth-1), [(getGamePos()[0][0], y), (getGamePos()[1][0], y+1)], 0)
##        win32api.SetCursorPos(t)
##        time.sleep(0.5)
##    return waypoints

def play(n=3, mode='hiscore'):
    global begin
    global end
    global buzzerPx
    
    tol = 0.42
    n = 120    
    print ("It starts...")
    setScreenSize()
    print "Screen size:", screenSize
    findGame(buzzerPx[0], buzzerPx[1])
    print "Found game at:", getGamePos()
    getLineWidth()
    for i in range(n):
        if mode == 'farm':
            '''Finish level two and suicide n times'''            
            print "Starting game..."
            startGame(buzzerMenu)
            clickRatio((0.76, 0.58))
            time.sleep(0.1)
            findInit()
            print "Begin:", begin
            findTarget()
            print "End:", end
            for i in range(2):
                print "Starting level", i
                time.sleep(1)
                clickRatio((0.76, 0.58))
                time.sleep(0.2)
                print "Generating path..."
                waypoints = createWaypoints(tol, n, (n-10))
                print "Sorting waypoints..."
                waypoints = sortWaypoints(waypoints)
                print "Pruning path..."
                path = pruneWaypoints(waypoints)
                path = removeDuplicates(path)
                print "Fine-tuning path..."
                path = [(begin[0]-getGamePos()[0][0],
                         begin[1]-getGamePos()[0][1])]+path[3:-3]+[(end[0]-getGamePos()[0][0],
                         end[1]-getGamePos()[0][1])]
                path = removeDuplicates(pruneWaypoints(sortWaypoints(avgPath(path))))
                walk = [begin]
                for i in range(len(path)-1):
                    segment = interpolate(path[i], path[i+1], 1)
                    walk += segment
                walk = removeDuplicates(walk)
##                print "Plotting graph..."
##                visualizer.setData(path, tol, n,
##                                   (begin[0]-getGamePos()[0][0], begin[1]-getGamePos()[0][1]),
##                                   (end[0]-getGamePos()[0][0], end[1]-getGamePos()[0][1]),
##                                   4)
##                visualizer.main()
##                time.sleep(0.1)
                print "Traversing path.."
                clickAbs(begin)
                typeStr('cheese')
                traversePath(path[1:]+[(end[0]-getGamePos()[0][0],
                             end[1]-getGamePos()[0][1]),],
                             getGamePos()[0], False, 0.024)
                print "Level", i, "finished."
            sudicide(begin)
        
        if mode == 'hiscore':
            '''Play as hard as possible n times'''            
            print "Starting game..."
            startGame(buzzerMenu)
            clickRatio((0.76, 0.58))
            time.sleep(0.1)
            findInit()
            print "Begin:", begin
            findTarget()
            print "End:", end
            for i in range(10):
                print "Starting level", i
                time.sleep(1)
                clickRatio((0.76, 0.58))
                time.sleep(0.2)
                print "Generating path..."
                waypoints = createWaypoints(tol, n, (n-10))
                print "Sorting waypoints..."
                waypoints = sortWaypoints(waypoints)
                print "Pruning path..."
                path = pruneWaypoints(waypoints)
                path = removeDuplicates(path)
                print "Fine-tuning path..."
                path = [(begin[0]-getGamePos()[0][0],
                         begin[1]-getGamePos()[0][1])]+path[3:-3]+[(end[0]-getGamePos()[0][0],
                         end[1]-getGamePos()[0][1])]
                path = removeDuplicates(pruneWaypoints(sortWaypoints(avgPath(path))))
                walk = [begin]
                for i in range(len(path)-1):
                    segment = interpolate(path[i], path[i+1], 1)
                    walk += segment
                walk = removeDuplicates(walk)
                print "Plotting graph..."
                visualizer.setData(path, tol, n,
                                   (begin[0]-getGamePos()[0][0], begin[1]-getGamePos()[0][1]),
                                   (end[0]-getGamePos()[0][0], end[1]-getGamePos()[0][1]),
                                   4)
                visualizer.main()
                time.sleep(0.1)
                print "Traversing path.."
                clickAbs(begin)
                typeStr('cheese')
                traversePath(path[1:]+[(end[0]-getGamePos()[0][0],
                             end[1]-getGamePos()[0][1]),],
                             getGamePos()[0], False, 0.024)
                print "Level", i, "finished."

##
##if __name__ == '__main__':
##    print ("It starts...")
##    setScreenSize()
##    print "Screen size:", screenSize
##    findGame(buzzerPx[0], buzzerPx[1])
##    print "Found game at:", getGamePos()
##    print "Starting game..."
##    startGame(buzzerMenu)
##    time.sleep(0.2)
##    findInit()
##    print "Begin:", begin
##    time.sleep(0.2)
##    
##    findTarget()
##    print "End:", end
##    getLineWidth()
##    tol = 0.42
##    n = 60#460
##    time.sleep(0.2)
##    print "Generating path..."
##    waypoints = createWaypoints(tol, n, (n-10))
##    print "Sorting waypoints..."
##    path = sortWaypoints(waypoints)
##    print "Pruning path..."
##    path = pruneWaypoints(path)
####    print "Plotting graph..."
####    visualizer.setData(path, tol, n, (begin[0]-getGamePos()[0][0], begin[1]-getGamePos()[0][1]), (end[0]-getGamePos()[0][0], end[1]-getGamePos()[0][1]))
####    visualizer.main()
####    time.sleep(0.5)
##    print "Traversing path.."
##    clickAbs(begin)
##    print path+[end[0]-getGamePos()[0][0], end[1]-getGamePos()[0][1]]
##    traversePath(path+[(end[0]-getGamePos()[0][0], end[1]-getGamePos()[0][1]),], getGamePos()[0], False, 0.1)#0.002
##    print "Done."
##
##
##
###, (0.085, 0.50), (0.94, 0.51)
##
##
##
##
##
## 
