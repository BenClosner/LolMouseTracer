# Ben Closner
# this file records mouse movements when executed and the user is playing the video game 'League of Legends'
# When the game is complete, it draws a graph of mouse movements, and a heatgraph of mouse areas.
# To use this tool, run the file. It will check to see if LoL is running every so often until the number of checks (
# default 2) has passed, then will exit if it is not. Then, the program records clicks until the game is exit.


import win32gui, win32api
import time
import matplotlib.pyplot as plt
import re
import numpy as np

def hit_it(minutes_to_check=2):
    for x in range(minutes_to_check + 1):
        if is_playing_league():    
            x,y = record_clicks()
            if len(x) > 1:
                make_graph(x,y)
                heat_graph(x,y)
                break
        else:
            print('Not playing leegue')
            checks = minutes_to_check - x
            if checks == 0:
                print('Finished')
            else:
                print('checking again in 20 seconds. {} more checks'.format(minutes_to_check - x))
                time.sleep(20)

def record_clicks():
    x_coords = []
    y_coords = []
    height_offset = win32api.GetSystemMetrics(1)
    x = 1
    while True:
        cursor = win32gui.GetCursorInfo()
        x_coords.append(cursor[2][0])
        y_coords.append(-cursor[2][1] + height_offset)
        time.sleep(0.05)
        if x % 50 == 0:
            if not is_playing_league():
                break
        x += 1
    return (x_coords, y_coords)

def make_graph(x_coords, y_coords):
    # draws a connect plot of mouse movements
    window_width = win32api.GetSystemMetrics(0)
    window_height = win32api.GetSystemMetrics(1)
    axis_ranges = [0, window_width, 0, window_height]
    plt.plot(x_coords, y_coords)
    plt.axis(axis_ranges)
    plt.show()

def heat_graph(x, y):
    # draws a heatmap of mouse locations
    heatmap, xedges, yedges = np.histogram2d(x,y,bins=50)
    window_width = win32api.GetSystemMetrics(0)
    window_height = win32api.GetSystemMetrics(1)
    axis_ranges = [0, window_width, 0, window_height]
    plt.clf()
    plt.imshow(heatmap, extent=axis_ranges)
    plt.show()
    
     
def is_playing_league():
    # Uses win32gui to get all open windows. Looks through this list of windows to check
    # if 'League of Legends' is among them. If it is, it return True.
    windows = []
    add = lambda x,y: y.append(x)
    win32gui.EnumWindows(add, windows)
    pattern = r'League of Legends'
    for window in windows:
        if win32gui.IsWindowVisible(window):
            text = win32gui.GetWindowText(window)
            if re.match(pattern, text):
                return True
    return False

if __name__ == '__main__':
    hit_it()
