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
from multiprocessing import Process, Manager, Lock
from time import time
from xl import make_csv

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


def start(process_list):
    for proc in process_list:
        proc.start()


def stop(process_list):
    for proc in process_list:
        proc.join()


if __name__ == "__main__":
    avg_wt = 0.6
    camera = cv2.VideoCapture(sys.argv[1])
    # camera = cv2.VideoCapture('data/Problem 2/slip.avi')
    # initialize num of frames
    num_frames = 0
    x1, x2, y1, y2 = [0]*4
    selected_partitions_global = []
    pool = Pool(processes=4)
    manager = Manager()

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
        # denoised_clone = utils.denoise(clone)

        start_time = time() # start time of partition functions

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
                # return segment coordinates cooresponding to a center value
                # map to all the functions
                # cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0))
                # get the mapper function to each segment
                print(len(selected_partitions_global))

                all_procs = [] # store processes to join
                return_list = manager.list()

                if len(selected_partitions_global) > 0:
                    for partition_number in selected_partitions_global.keys():
                        print(partition_number)

                        def wrapper(func, frame_no, partition_number, coords, frame, ret_list):
                            map_ret = func(coords, frame)
                            obj = {
                                'fno': frame_no,
                                'pno': partition_number,
                                'coords': coords,
                                'return': map_ret
                            }
                            print(map_ret)

                            return_list.append(obj)

                        targt_func_args = (mapper_func[partition_number], num_frames, partition_number, 
                            selected_partitions_global[partition_number], frame, return_list)
                        all_procs.append(Process(target=wrapper, args=targt_func_args))

                        # all_procs.append(Process(target=mapper_func[partition_number], 
                        #     args=(selected_partitions_global[partition_number], frame)))

                        # mapper_return = mapper_func[partition_number](selected_partitions_global[partition_number], frame)
                        # print("Partition: ", partition_number, "Output: ", mapper_return)
                        # x1, y1, x2, y2 = selected_partitions_global[partition_number]
                        # cv2.rectangle(denoised_clone, (x1, y1), (x2, y2), (0, 255, 0), 5)

                start(all_procs)
                stop(all_procs)

                print('Printing return list: ', return_list)
		make_csv(num_frames, return_list)
                end_time = time() # start time of partition functions

                print('Time taken for the frame: ', (end_time - start_time))

                # cv2.imshow("Thesholded", thresholded)
                # x1, y1, x2, y2 = selected_partitions_global[list(selected_partitions_global.keys())[0]]
                # cv2.rectangle(denoised_clone, (x1,y1),(x2,y2), (0,255,0), 5)



        num_frames = (num_frames+1)%200

        # display the frame with segmented hand
        # cv2.imshow("Video Feed", clone)


        # cv2.rectangle(clone, (x1, y1), (x2, y2), (255, 0, 0))
        # observe the keypress by the user
        # keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        # if keypress == ord("q"):
        #     break

    camera.release()
    cv2.destroyAllWindows()
