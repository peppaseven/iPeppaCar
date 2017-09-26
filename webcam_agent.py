import os
import cv2
import time
import argparse
import multiprocessing
import numpy as np
import requests
import json
import io
from PIL import Image
from utils.webcam_utils import MJPEGWebcamVideoStream
from multiprocessing import Queue, Pool
from utils.tempimage import TempImage
from utils.tts import BaiduTTS
CWD_PATH = os.getcwd()

def detect_objects(image_np, conf):
    # write the image to temporary file
    pil_image = Image.fromarray(image_np)
    pil_image_resized = pil_image.resize((320, 240), Image.ANTIALIAS)
    np_frame = np.array(pil_image_resized)

    t = TempImage()
    cv2.imwrite(t.path, np_frame)
    tf_server_ip = conf["tf_classify_server"]
    tf_classify_url = 'http://{ip}/classify_image'.format(ip=tf_server_ip)
    imagefile = {'imagefile': open(t.path, 'rb')}
    resp = requests.post(tf_classify_url, files=imagefile)
    t.cleanup()
    if resp.json()['has_result']:
        print(resp.json()['name'])
        cv2.putText(image_np, "Object is: {}".format(resp.json()['name']), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)

    return image_np,resp.json()['has_result'],resp.json()['name']


def worker(input_q, output_q,conf):
    object_name = ''
    try:
        while True:
            np_frame = input_q.get()
            image_np,result,label_name=detect_objects(np_frame,conf)
            if result:
                if not (object_name == label_name):
                    object_name = label_name
                    if conf["speak_result"]:
                        print('speak object: %s' %(object_name))
                        api_key = conf["baidu_tts_apikey"]
                        secret_key = conf["baidu_tts_secretkey"]
                        tts = BaiduTTS(api_key, secret_key)
                        tts.say(object_name)

            output_q.put(image_np)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print('Child exit,parent received ctrl-c')

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

    # initialize the first frame in the video stream
    first_frame = None
    try:
        while True:  # fps._numFrames < 120
            frame = video_capture.read()

            if conf["use_moving_detection"]:
                data_stream = io.BytesIO(frame)
                # open as a PIL image object
                pil_image = Image.open(data_stream).convert('RGB')
                np_frame = np.array(pil_image)
                gray = cv2.cvtColor(np_frame, cv2.COLOR_RGB2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                # if the first frame is None, initialize it
                if first_frame is None:
                    input_q.put(np_frame)
                    first_frame = gray
                    continue
                # compute the absolute difference between the current frame and
                # first frame
                frameDelta = cv2.absdiff(first_frame, gray)
                #print(frameDelta)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

                # dilate the thresholded image to fill in holes, then find contours
                # on thresholded image
                thresh = cv2.dilate(thresh, None, iterations=2)
                (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
                # loop over the contours
                is_new_obj = False
                for c in cnts:
                    # if the contour is too small, ignore it
                    if cv2.contourArea(c) < conf["min_area"]:
                        continue

                    # compute the bounding box for the contour, draw it on the frame,
                    # and update the text
                    (x, y, w, h) = cv2.boundingRect(c)
                    #print("Rect:x-{},y-{},w-{},h-{}".format(x,y,w,h))
                    is_new_obj = True
                if is_new_obj:
                    input_q.put(np_frame)

            else:
                data_stream = io.BytesIO(frame)
                # open as a PIL image object
                pil_image = Image.open(data_stream).convert('RGB')
                np_frame = np.array(pil_image)
                # check moving object,then put it to input queue
                input_q.put(np_frame)


            # check to see if the frames should be displayed to screen
            if conf["show_video"]:
                frame = output_q.get()
                # display the security feed
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imshow("Object Detector", frame)

            key = cv2.waitKey(1) & 0xFF
            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                break

    except KeyboardInterrupt:
        print('parent received ctrl-c')
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


