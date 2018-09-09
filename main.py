import imutils
from mapper import *
import utils
from segment import *
import cv2
import imutils
import sys
import numpy as np
from sklearn.metrics import pairwise
import utils


img = None

mapper_func = {
    "2": VTA_2,
    "3": AirSpeed_3,
    "4": Baro_4,
    "5": ICE_5,
    "6": LAT_6,
    "7": VSP_7,
    "8": Compass_8,
    "9": Wind_9,
    "10": Slip_9
}


if __name__ == "__main__":
    avg_wt = 0.6
    camera = cv2.VideoCapture(sys.argv[1])
    # camera = cv2.VideoCapture('data/Problem 2/slip.avi')
    # initialize num of frames
    num_frames = 0
    x1, x2, y1, y2 = [0]*4
    selected_partitions_global = []
    while True:
        # current frame
        ret_value, frame = camera.read()

        if ret_value == False:
            break

        # frame = imutils.resize(frame, width=700)
        clone = frame[:, :]
        # get the height and width of the frame
        (height, width) = frame.shape[:2]
        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        thresh = cv2.erode(gray, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)

        # calibrating our running average until a threshold is reached
        denoised_clone = utils.denoise(clone)


        if num_frames < 6:
            running_avg(thresh, avg_wt)

        else:
            seg_img = segment(thresh)

            if seg_img is not None:
                # i.e. if segmented
                (thresholded, segmented) = seg_img
                # print("Center", center)
                if num_frames < 50:
                    selected_partitions = utils.segment_divider(thresholded)
                    if len(selected_partitions_global) < len(selected_partitions):
                        selected_partitions_global = selected_partitions

                # get the mapper function to each segment
                print(len(selected_partitions_global))
                if len(selected_partitions_global) > 0:
                    for partition_number in selected_partitions_global.keys():
                        print(partition_number)
                        mapper_return = mapper_func[partition_number](selected_partitions_global[partition_number], denoised_clone)
                        print("Partition: ", partition_number, "Output: ", mapper_return)
                        x1, y1, x2, y2 = selected_partitions_global[partition_number]
                        cv2.rectangle(denoised_clone, (x1, y1), (x2, y2), (0, 255, 0), 5)

                # cv2.imshow("Thesholded", thresholded)

                cv2.imshow("Denoised Video", denoised_clone)



        num_frames = (num_frames+1)%200

        # display the frame with segmented hand
        # cv2.imshow("Video Feed", clone)


        # cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0))
        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
