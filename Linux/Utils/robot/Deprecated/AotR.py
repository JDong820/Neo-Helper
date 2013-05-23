from Neo2 import *

def easy():
    wait(4)
    for i in range(1000):
        cmd = 'space', 'up', 'space', 'down', 'space', 'left', 'up', 'space', 'down', 'right', 'space', 'left', 'left', 'up', 'space', 'down', 'right', 'right', 'space', 'left', 'left', 'left', 'up', 'space', 'down', 'right', 'right', 'right'
        for c in cmd:
            if c == 'space':
                pressKey(c, 1, 0, 0.5)
            else:
                pressKey(c, 1, 0, 0.001)
    
