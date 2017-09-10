# From http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/

import urllib2
import base64
import datetime
from threading import Thread
import time

class MJPEGWebcamVideoStream:
    def __init__(self, ip, username, password, num,interval):
        # initialize the video camera stream and read the first frame
        # from the stream
        url= 'http://{ip}/?action=snapshot_{num}'.format(ip=ip,num=num)
        auth_str = base64.b64encode('%s:%s' % (username, password))
        self.request = urllib2.Request(url)
        self.request.add_header("Authorization", "Basic %s" % auth_str)
        self.interval = interval;
        #first frame
        #start = time.time()
        stream = urllib2.urlopen(self.request)
        self.frame = stream.read()
        #diff = time.time() -start
        #print('%0.3f s' %(diff))
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            try:
                stream = urllib2.urlopen(self.request)
                self.frame = stream.read()
            except urllib2.HTTPError as e:
                print(e.reason)
            if self.interval>0:
                time.sleep(self.interval)
    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True