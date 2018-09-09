def lat(coord, frame):
    from utils import threshold
    import numpy as np

    lat = frame[coord[1]:coord[-1], coord[0]:coord[-2]]
    t = threshold(np.asarray(image)[34:45,50:222])
    n = np.where(t==True)
    y = sum(n[1])/len(n[1])
    return (y/160 * 20) - 10
