'''
Module receives frames from the agora api and applies
 algorithm to every frame. Script emulates a browser
in the python script on a server and parses frames off it
'''

import argparse
import numpy as np
import asyncio
import time
from PIL import Image
import io
from darkflow.net.build import TFNet
import cv2
from Algorithms import conversion
from dbinit import db


def get_pred(img):
    # preds = tfnet.return_predict(img)
    results = []

    for pred in preds:
        if pred['label'] != 'person':
            continue

        result = {}
        result['tl'] = [pred['topleft']['x'], pred['topleft']['y']]
        result['br'] = [pred['bottomright']['x'], pred['bottomright']['y']]
        results.append(result)

    return results


def save(img, writer):
    writer.write(img)
    # cv2.imwrite('output.jpg', img)


def main():
    cap = cv2.VideoCapture('drone.mov')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 30, (1920,1080))
    cnt = 0

    print('Reading video and applying YOLO')
    while(cap.isOpened() and cnt < 10000):
        ret, frame = cap.read()

        if not ret:
            continue

        out_img = # call the algorithm here
        
        print('\r'+str(cnt)+':'+str(len(pred)), end='')
        cnt += 1

        # save(out_img, out)

    cap.release()
    out.release()


if __name__ == '__main__':
    main()
