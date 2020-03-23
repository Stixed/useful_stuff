import numpy as np
from matplotlib.animation import FuncAnimation

def reading(fname):
    data = np.genfromtxt(fname, dtype = float, delimiter = ',')
    print(data)
    return data

def getPoints(points, center, radiusX = 0.01, radiusY = 20):
    outData = []
    n = 0
    
    print("{} points was added".format(n))
    return outData

# def reading2(fname):
#     f = open(fname)
#     for line in f.readlines():
#         print (line)
#     f.close()
#     return data
def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    X,Y = getPoints(point,[event.xdata, event.ydata])
    outX.extend(X)
    outY.extend(Y)

def update():

    return ln,
def main():
    
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    return None
