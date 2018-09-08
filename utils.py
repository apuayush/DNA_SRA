def segment(image):
    from skimage.filters import threshold_minimum
    import numpy as np

    image = np.dot(image[...,:3], [0.299, 0.587, 0.114])
    thresh = threshold_minimum(np.asarray(image)[:,:,0])
    return np.asarray(image)[:,:,0] > thresh
