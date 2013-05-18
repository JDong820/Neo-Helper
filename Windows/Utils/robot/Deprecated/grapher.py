from Tkinter import *

name = ''
lines = []
points = []
specialPoints = []
zoom = 1

def setData(n, l, p, pBold, z=1):
    global name
    global lines
    global points
    global specialPoints
    global zoom

    name = n
    lines = l[:]
    points = p[:]
    specialPoints = pBold[:]
    zoom = z
    
def main():
    global name
    global lines
    global points
    global specialPoints
    global zoom
    
    root = Tk()
    root.title(name)

    try:
        canvas = Canvas(root, width=1100, height=600, bg = 'white')
        canvas.pack()
        Button(root, text='Quit', command=root.quit).pack()
        Button(root, text='+').pack()#, command=zoomIn).pack()
        Button(root, text='-').pack()#, command=zoomOut).pack()

        pointZ = []
        specialZ = []
        lineZ = []
        for l in lines:
            lineZ.append(((l[0][0]*zoom, l[0][1]*zoom), (l[1][0]*zoom, l[1][1]*zoom)))
        for p in points:
            pointZ.append((p[0]*zoom, p[1]*zoom))
        for p in specialPoints:
            specialZ.append((p[0]*zoom, p[1]*zoom))

##        print "Drawing lines..."
##        for i in range(len(lines)-1):
##            if i == 0:
##                canvas.create_line(points[i][0], points[i][1], pointZ[i+1][0], pointZ[i+1][1], width=1, fill='blue')
##            else:
##                canvas.create_line(points[i][0], points[i][1], points[i+1][0], pointZ[i+1][1], width=1, fill='black')
        print "Plotting lines..."
        for p1, p2 in lineZ:
            canvas.create_line(p1[0],p1[1],p2[0],p2[1], width=1, fill='black')
        print "Plotting points..."
        for x,y in pointZ:
            canvas.create_oval(x-1,y-1,x+1,y+1, width=0, fill='red')
        print "Plotting special points..."
        for x,y in specialZ:
            canvas.create_oval(x-3,y-3,x+3,y+3, width=1, fill='green')
        
    except:
        print 'An error has occured!'
        #quit()
    root.mainloop()

if __name__ == '__main__':
    main()
