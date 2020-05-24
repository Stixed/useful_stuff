import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import sys
# from pynput.keyboard import Key, Listener

def reading(fname):
    data = np.loadtxt(fname, dtype = float, delimiter = ',')
    print(data)
    return data

def check(x, x0, deltax):
    if x <= x0+deltax and x>=x0-deltax:
        return True
    else:
        return False
    

def getPoints(points, center):
    outData = np.zeros((1,4))
    # outData = []
    global radiusX, radiusY
    n = 0
    for i in range(len(points[:,0])):
        #print(points[i,:])
        if check(points[i, 1], center[0], radiusX) and check(points[i, 2], center[1], radiusY):
            outData = np.append(outData, [points[i,:]], axis = 0)
            n += 1
    outData = np.delete(outData, 0, 0)
    print("{} points was added".format(n))
    return outData

# def on_press(key):
#     print('{0} pressed'.format(
#         key))

# def on_release(key):
#     print('{0} release'.format(
#         key))
#     if key == Key.esc:
#         # Stop listener
#         return False


print('File to open:')    
fname = input()
print('File to save the chosen data:')
fnameOut = input()
points = reading(fname)
saveData = np.zeros((1,4))
radiusX = 0.01
radiusY = 20
# print(saveData)
fig, ax = plt.subplots()
def onclick(event):
    global saveData
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    chosenPoints = getPoints(points,[event.xdata, event.ydata])
    saveData = np.append(saveData, chosenPoints, axis = 0)

def press(event):
    global radiusX, radiusY 
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'right':
        radiusX *= 1.1
        print('increase delta X ', radiusX)
    if event.key == 'left':
        radiusX /= 1.1
        print('decrease delta X', radiusX)
    if event.key == 'up':
        radiusY *= 1.1
        print('increase delta Y', radiusY)
    if event.key == 'down':
        radiusY /= 1.1
        print('decrease delta Y', radiusY)
def handle_close(evt):
    new_array = [tuple(row) for row in saveData]
    new_SaveData = np.unique(new_array, axis = 0)
    np.savetxt(fnameOut, new_SaveData, delimiter=',')


cid = fig.canvas.mpl_connect('button_press_event', onclick)
cib = fig.canvas.mpl_connect('close_event', handle_close)
cic = fig.canvas.mpl_connect('key_press_event', press)
plt.plot(points[:,1], points[:,2], '.')
plt.ylim((100,2600))
plt.show()

# with Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

# plt.plot(points[:,0], points[:,2], '.')
# plt.ylim((100,2600))
# plt.show()

