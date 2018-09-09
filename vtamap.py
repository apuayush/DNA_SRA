def vta(coord, frame):
    from utils import threshold
    import numpy as np

    img = frame[coord[1]:coord[-1], coord[0]:coord[-2]]
    img = threshold(img)

    return np.count_nonzero(img)/(img.shape[0]*img.shape[1]) >= 0.1
