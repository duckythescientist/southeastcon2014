#!/usr/bin/env python

import subprocess
import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>]
'''

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

if __name__ == '__main__':
    import sys, getopt, os, signal, time
    print help_message

    imfile = "/dev/shm/camcap.jpg"

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade='])
    try: video_src = video_src[0]
    except: video_src = 0
    args = dict(args)
    cascade_fn = args.get('--cascade', "data/haarcascades/haarcascade_frontalface_default.xml")
    
    cascade = cv2.CascadeClassifier(cascade_fn)
    
    # cam = create_capture(video_src, fallback='synth:bg=../cpp/lena.jpg:noise=0.05')
    f = open("/tmp/raspifastcamd.pid")
    pid = int(f.readline())
    print "pid is: ", pid
    f.close()
    if os.path.exists(imfile):
        os.remove(imfile)
    os.kill(pid, signal.SIGUSR1)
    time.sleep(0.5)

    while True:
        img = cv2.imread(imfile)
        os.kill(pid, signal.SIGUSR1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.equalizeHist(gray)

        t = clock()
        rects = detect(gray, cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        
        dt = clock() - t

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)
        # time.sleep(0.3)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()

