from utils import threshold
import numpy as np


def VTA_2(coord, frame):
    img = frame[coord[1]:coord[-1], coord[0]:coord[-2]]
    img = threshold(img)

    return np.count_nonzero(img)/(img.shape[0]*img.shape[1]) >= 0.1


def ICE_5(coord, frame):
    x1, y1, x2, y2 = coord
    roi = frame[y1: y2, x1: x2]

    p = np.count_nonzero(roi > 200)

    return p/frame.shape >= 0.15