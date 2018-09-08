from skimage.filters import threshold_minimum
import numpy as np
import cv2


def segment(image):
    image = np.dot(image[...,:3], [0.299, 0.587, 0.114])
    thresh = threshold_minimum(np.asarray(image)[:,:,0])
    return np.asarray(image)[:,:,0] > thresh


def denoise(image):
    """ Bilateral filtering with opencv on image segments
    """
    new = cv2.bilateralFilter(image, 9, 75, 75)
    return new
