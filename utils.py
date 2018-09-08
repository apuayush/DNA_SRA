from skimage.filters import threshold_minimum
import numpy as np
import cv2
def threshold(image):
    """ Does thresholding
    """
    from skimage.filters import threshold_minimum
    import numpy as np    

    image = np.asarray(img)
    image = np.dot(image[...,:3], [0.299, 0.587, 0.114])
    thresh = threshold_minimum(image[:,:])
    return image[:,:] > thresh

def denoise(image):
    """ Bilateral filtering with opencv on image segments
    """
    new = cv2.bilateralFilter(image, 9, 75, 75)
    return new
