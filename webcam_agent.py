import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import json
import io
from PIL import Image
from utils.webcam_utils import MJPEGWebcamVideoStream
from multiprocessing import Queue, Pool

CWD_PATH = os.getcwd()

def detect_objects(image_np,conf):

    return image_np


def worker(input_q, output_q,conf):
    while True:
        image_bytes = input_q.get()
        data_stream = io.BytesIO(image_bytes)
        # open as a PIL image object
        pil_image = Image.open(data_stream).convert('RGB')
        pil_image_resized = pil_image.resize((320,240), Image.ANTIALIAS)
        np_frame = np.array(pil_image_resized)
        output_q.put(detect_objects(np_frame,conf))

def agent_start(num_workers,queue_size,conf_path):

    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)

    conf = json.load(open(conf_path))
    input_q = Queue(maxsize=queue_size)
    output_q = Queue(maxsize=queue_size)
    pool = Pool(num_workers, worker, (input_q, output_q,conf))


    #ip camera
    ip = conf["webcam_ip"]
    username = conf["webcam_user"]
    passwd = conf["webcam_pwd"]
    which_cam = conf["webcam_num"]
    interval = conf["webcam_query_interval"]
    #print('ip:{ip},username:{username}'.format(ip=ip,username=username))
    video_capture = MJPEGWebcamVideoStream(ip,username,passwd,which_cam,interval).start()

    while True:  # fps._numFrames < 120
        frame = video_capture.read()
        input_q.put(frame)

        frame = output_q.get()

        # check to see if the frames should be displayed to screen
        if conf["show_video"]:
            # display the security feed
            cv2.imshow("Video", frame)
            key = cv2.waitKey(1) & 0xFF
            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                break

    pool.terminate()
    video_capture.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-num-w', '--num-workers', dest='num_workers', type=int,
                        default=2, help='Number of workers.')
    parser.add_argument('-q-size', '--queue-size', dest='queue_size', type=int,
                        default=5, help='Size of the queue.')
    parser.add_argument("-c", "--conf", required=True,
                    help="path to the JSON configuration file")


    args = parser.parse_args()

    agent_start(args.num_workers,args.queue_size,args.conf)


