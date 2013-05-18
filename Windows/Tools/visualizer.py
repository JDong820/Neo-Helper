from Tkinter import *

visualPoints = []
name = []
endpoints = []
zoom = 1

def setData(ps, t, n, b, e, z=1):
    global visualPoints
    global name
    global endpoints
    global zoom
    
    visualPoints = ps[:]
    name = t,n
    endpoints = [b,e]
    zoom = z
    
def main():
    global visualPoints
    global name
    global endpoints
    global zoom
    
    root = Tk()
    root.title('BuzzerPath--Tolerence:'+str(name[0])+'--Resolution:'+str(name[1]))

    try:

        canvas = Canvas(root, width=1200, height=700, bg = 'white')
        canvas.pack()
        Button(root, text='Quit', command=root.quit).pack()

        if zoom != 1:
            print "zoom:", zoom
            for i in range(len(visualPoints)):
                visualPoints[i] = (visualPoints[i][0]*zoom, visualPoints[i][1]*zoom)
            for i in range(len(endpoints)):
                endpoints[i] = (endpoints[i][0]*zoom, endpoints[i][1]*zoom)

        print "Drawing lines..."
        for i in range(len(visualPoints)-1):
            if i == 0:
                canvas.create_line(visualPoints[i][0], visualPoints[i][1], visualPoints[i+1][0], visualPoints[i+1][1], width=1, fill='blue')
            else:
                canvas.create_line(visualPoints[i][0], visualPoints[i][1], visualPoints[i+1][0], visualPoints[i+1][1], width=1, fill='black')
        print "Plotting points..."
        for x,y in visualPoints:
            canvas.create_oval(x-1,y-1,x+1,y+1, width=0, fill='red')
        print "Plotting endpoints..."
        for x,y in endpoints:
            canvas.create_oval(x-3,y-3,x+3,y+3, width=1, fill='green')        
    except:
        print 'An error has occured!'
    root.mainloop()

if __name__ == '__main__':
    main()
