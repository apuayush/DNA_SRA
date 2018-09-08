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

def segment_divider(thresholded_frame):
    """
    return segment coordinates cooresponding to a center
    :param center:
    :return:
    """
    segments = []
    selected_partition = []
    with open('admin_tools/imgs/img.json', 'r') as f:
        segments = json.load(f)
    for single_seg in segments.keys():
        try:
            x1, y1, x2, y2 = segments[single_seg]
            cropped_image = thresholded_frame[y1:y2, x1:x2]

            bench = np.count_nonzero((170 < cropped_image))
            # print(bench/ thresholded_frame.size)
            if bench/ cropped_image.size > 0.0001:
                selected_partition.append({single_seg: [x1,y1,x2,y2]})
        except: pass


    return selected_partition





