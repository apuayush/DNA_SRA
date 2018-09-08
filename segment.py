# libraries
import cv2
import imutils
import sys
import numpy as np
from sklearn.metrics import pairwise

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
        segmented = min(cnts, key=cv2.contourArea)
        return (thresholded, segmented)


def detect_moving_object(thresholded, segmented):
    cdnt_obj = []
    con_hull = cv2.convexHull(segmented)
    print("Hull:", len(con_hull))

    # find left right top bottom convex hull points
    for i in range(len(con_hull)):
        extreme_top = tuple(con_hull[con_hull[:, :, 1].argmin()][i])
        extreme_bottom = tuple(con_hull[con_hull[:, :, 1].argmax()][i])
        extreme_left = tuple(con_hull[con_hull[:, :, 0].argmin()][i])
        extreme_right = tuple(con_hull[con_hull[:, :, 0].argmax()][i])
        center_X = (extreme_left[0] + extreme_right[0]) // 2
        center_Y = (extreme_top[0] + extreme_bottom[0]) // 2

        #  find max distance b/w center and a convex_hull point
        distance = pairwise.euclidean_distances([(center_X, center_Y)],
                                                Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
        # Coordinates of moving object
        k = [extreme_left, extreme_right, extreme_bottom, extreme_top]
    cdnt_obj.append(k)
    print("cdnt obj",cdnt_obj)
    return cdnt_obj, distance


if __name__ == "__main__":
    avg_wt = 0.3
    # camera = cv2.VideoCapture(sys.argv[1])
    camera = cv2.VideoCapture('data/Problem 2/Altitude_Digits.avi')
    # initialize num of frames
    num_frames = 0

    while True:
        # current frame
        ret_value, frame = camera.read()
        if ret_value == False:
            break

        frame = imutils.resize(frame, width=700)
        # flip the frame to remove mirror view
        clone = frame.copy()
        # get the height and width of the frame
        (height, width) = frame.shape[:2]
        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # calibrating our running average until a threshold is reached

        if num_frames < 6:
            running_avg(gray, avg_wt)

        else:
            seg_img = segment(gray)

            if seg_img is not None:
                # i.e. if segmented
                (thresholded, segmented) = seg_img

                # draw segment region and display the frame
                cdnt_obj, distance = detect_moving_object(thresholded, segmented)
                alpha = 10
                for i in range(len(cdnt_obj))
                    x1, y1 = cdnt_obj[i][0][0]-alpha, cdnt_obj[i][3][1]+alpha
                    x2, y2 = cdnt_obj[i][1][0]+alpha, cdnt_obj[i][2][1]-alpha
                    # print("Points",x1,y1,x2,y2)
                    cv2.rectangle(thresholded, (x1, y1), (x2, y2), (255, 255, 255))
                cv2.imshow("Thesholded", thresholded)

        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
