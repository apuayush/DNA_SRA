def segment(image):
    from skimage.filters import threshold_minimum
    import numpy as np

    thresh = threshold_minimum(np.asarray(image)[:,:,0])
    return np.asarray(image)[:,:,0] > thresh
