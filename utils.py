from skimage.filters import threshold_minimum
import numpy as np
import cv2
import json

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

def segment_divider(center):
    """
    return segment coordinates cooresponding to a center
    :param center:
    :return:
    """
    segments = None
    with open('admin_tools/imgs/img.json', 'r') as f:
        segments = json.load(f)

    # print(segments)
    for single_seg in segments.keys():
        seg_coords = segments[single_seg]
        k = [center[0]-seg_coords[0], seg_coords[1]-center[1], seg_coords[2]-center[0], center[1]-seg_coords[3]]

        if min(k)>=0:
            return single_seg, seg_coords




