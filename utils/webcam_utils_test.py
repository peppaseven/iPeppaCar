# From http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
from webcam_utils import MJPEGWebcamVideoStream
import cv2
import time
import io
from PIL import Image
import numpy
if __name__ == '__main__':
    ip = "127.0.0.1:20081"
    username = "peter"
    passwd = "hitv"
    which_cam = 0

    video_capture = MJPEGWebcamVideoStream(ip, username, passwd, which_cam,0.05).start()

    while True:
        #add a delay for raspberry Pi3 CPU load
        time.sleep(0.05)
        image_bytes = video_capture.read()
        data_stream = io.BytesIO(image_bytes)
        # open as a PIL image object
        pil_image = Image.open(data_stream).convert('RGB')
        pil_image_resized = pil_image.resize((320,240), Image.ANTIALIAS)

        w, h = pil_image_resized.size
        print("w:%d,h:%d" %(w,h))

        frame = numpy.array(pil_image_resized)
        # Convert RGB to BGR
        frame = frame[:, :, ::-1].copy()
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.stop()
            break
    cv2.destroyAllWindows()