import os
import sys
import json
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector


img = None
tl_list = []
br_list = []
object_list = []

image_folder = '' + sys.argv[1]
save_dir = 'annotations_' + sys.argv[1]
obj = sys.argv[1]

print(obj)

segments = []

def line_select_callback(clk, rls):
    global tl_list
    global br_list
    tl_list.append((int(clk.xdata),int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))
    segments.append([int(clk.xdata),int(clk.ydata),int(rls.xdata), int(rls.ydata)])
    print(segments[-1])


def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == 'q':
        with open('coords.json', 'w') as f:
            json.dump(segments, f)
        print(segments)
        plt.close()
        sys.exit()

def toggle_selector(event):
    toggle_selector.RS.set_active(True)

if __name__ == "__main__":
    for n, image_file in enumerate(os.scandir(image_folder)):
        img = image_file
        fig, ax = plt.subplots(1)

        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)
        toggle_selector.RS =RectangleSelector(
            ax, line_select_callback,
            drawtype='box', useblit=True,
            button=[1], minspanx=5,minspany=5,
            spancoords='pixels', interactive=True
        )

        bbox = plt.connect('key_press_event', toggle_selector)
        key = plt.connect('key_press_event', onkeypress)
        plt.show()

