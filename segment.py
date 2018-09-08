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


def detect_moving_object(thresholded, segmented):

    # con_hull = cv2.convexHull(segmented)
    print(len(con_hull))

    # find left right top bottom convex hull points
    extreme_top = tuple(con_hull[con_hull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(con_hull[con_hull[:, :, 1].argmax()][0])
    extreme_left = tuple(con_hull[con_hull[:, :, 0].argmin()][0])
    extreme_right = tuple(con_hull[con_hull[:, :, 0].argmax()][0])
    center_X = (extreme_left[0] + extreme_right[0]) // 2
    center_Y = (extreme_top[1] + extreme_bottom[1]) // 2
    center = [center_X, center_Y]

    #  find max distance b/w center and a convex_hull point
    distance = pairwise.euclidean_distances([(center_X, center_Y)],
                                            Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    # Coordinates of moving object
    cdnt_object = [extreme_left, extreme_right, extreme_bottom, extreme_top]
    # print("cdnt_object:",cdnt_object)
    return cdnt_object, distance, center


if __name__ == "__main__":
    avg_wt = 0.6
    camera = cv2.VideoCapture(sys.argv[1])
    # camera = cv2.VideoCapture('data/Problem 2/slip.avi')
    # initialize num of frames
    num_frames = 0
    x1, x2, y1, y2 = [0]*4
    while True:
        # current frame
        ret_value, frame = camera.read()

        if ret_value == False:
            break

        # frame = imutils.resize(frame, width=700)
        # flip the frame to remove mirror view
        clone = frame.copy()
        # get the height and width of the frame
        (height, width) = frame.shape[:2]
        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        thresh = cv2.erode(gray, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)

        # calibrating our running average until a threshold is reached

        if num_frames < 6:
            running_avg(thresh, avg_wt)

        else:
            seg_img = segment(thresh)

            if seg_img is not None:
                # i.e. if segmented
                (thresholded, segmented) = seg_img

                # draw segment region and display the frame
                cdnt_obj, distance, center = detect_moving_object(thresholded, segmented)
                alpha = 10
                x1, y1 = cdnt_obj[0][0], cdnt_obj[3][1]
                x2, y2 = cdnt_obj[1][0], cdnt_obj[2][1]
                # print("Center", center)

                # seg_no, seg_coords = utils.segment_divider(center)
                # return segment coordinates cooresponding to a center value
                # map to all the functions
                """ TODO  -
                1 - pass clone to denoise - done
                2 - detect which segment through the center of the segment 
                3 - use each mapper function to make meaning of each segment change and save it in excel too 
                4 - 
                """
                # print("segmentation", seg_no, seg_coords)
                # cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0))
                cv2.imshow("Thesholded", thresholded)

        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)
        denoised_clone = utils.denoise(clone)
        cv2.imshow("Denoised Video", denoised_clone)

        # cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0))
        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
