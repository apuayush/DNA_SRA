from utils import threshold
import numpy as np
import cv2
import imutils


def VTA_2(coord, frame):
    img = frame[coord[1]:coord[-1], coord[0]:coord[-2]]
    img = threshold(img)

    return np.count_nonzero(img)/(img.shape[0]*img.shape[1]) >= 0.1


def AirSpeed_3(coord, frame):
    return 1


def Baro_4(coord, frame):
    return 1


def ICE_5(coord, frame):
    x1, y1, x2, y2 = coord
    roi = frame[y1: y2, x1: x2]

    p = np.count_nonzero(roi > 200)

    return p/frame.shape >= 0.15


def LAT_6(coord, frame):

    lat = frame[coord[1]:coord[-1], coord[0]:coord[-2]]
    t = threshold(np.asarray(frame)[34:45, 50:222])
    n = np.where(t == True)
    y = sum(n[1])/len(n[1])
    return (y/160 * 20) - 10

def VSP_7(coord, frame):
    return 1

def Compass_8(coord, frame):
    return 1

def Wind_9(coord, frame):
    return 1

def Slip_9(coord, frame):

    slip = frame[coord[1]:coord[-1], coord[0]:coord[-2]]
    gray = cv2.cvtColor(slip, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    m = 0
    for c in cnts:
        M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    m = max(abs(cX - 123), m)

    return m / 123 * 100

def alt_digit(coords, frame):
    return 1
