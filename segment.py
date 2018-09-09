# libraries
import cv2
import imutils
import sys
import numpy as np
from sklearn.metrics import pairwise
import utils

bg = None


def running_avg(img, avg_wt):
    global bg

    # for the first time
    if bg is None:
        bg = img.copy().astype('float')
        return

    # accumulating weighted average and updating the background
    cv2.accumulateWeighted(img, bg, avg_wt)


def segment(img, threshold=25):
    global bg
    # absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), img)

    # to get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # contours
    (_, cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        # for no contour
        return
    else:
        # maximum contour area
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

# if __name__ == "__main__":
#     avg_wt = 0.6
#     camera = cv2.VideoCapture(sys.argv[1])
#     # camera = cv2.VideoCapture('data/Problem 2/slip.avi')
#     # initialize num of frames
#     num_frames = 0
#     x1, x2, y1, y2 = [0]*4
#     selected_partitions_global = []
#     while True:
#         # current frame
#         ret_value, frame = camera.read()
#
#         if ret_value == False:
#             break
#
#         # frame = imutils.resize(frame, width=700)
#         # flip the frame to remove mirror view
#         clone = frame.copy()
#         # get the height and width of the frame
#         (height, width) = frame.shape[:2]
#         # convert the roi to grayscale and blur it
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         gray = cv2.GaussianBlur(gray, (7, 7), 0)
#         thresh = cv2.erode(gray, None, iterations=2)
#         thresh = cv2.dilate(thresh, None, iterations=4)
#
#         # calibrating our running average until a threshold is reached
#
#         if num_frames < 6:
#             running_avg(thresh, avg_wt)
#
#         else:
#             seg_img = segment(thresh)
#
#             if seg_img is not None:
#                 # i.e. if segmented
#                 (thresholded, segmented) = seg_img
#                 # print("Center", center)
#                 if num_frames < 20:
#                     selected_partitions = utils.segment_divider(thresholded)
#                     if len(selected_partitions_global) < len(selected_partitions):
#                         selected_partitions_global = selected_partitions
#                 # return segment coordinates cooresponding to a center value
#                 # map to all the functions
#                 """
#                 3 - use each mapper function to make meaning of each segment change and save it in excel too
#                 4 -
#                 """
#
#                 # cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0))
#                 cv2.imshow("Thesholded", thresholded)
#
#         num_frames = (num_frames+1) % 200
#
#         # display the frame with segmented hand
#         cv2.imshow("Video Feed", clone)
#         denoised_clone = utils.denoise(clone)
#         cv2.imshow("Denoised Video", denoised_clone)
#
#         # cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0))
#         # observe the keypress by the user
#         keypress = cv2.waitKey(1) & 0xFF
#
#         # if the user pressed "q", then stop looping
#         if keypress == ord("q"):
#             break
#
#     camera.release()
#     cv2.destroyAllWindows()
