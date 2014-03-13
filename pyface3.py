#!/usr/bin/env python

import subprocess
import numpy as np
import cv2
import cv2.cv as cv
from video import create_capture
from common import clock, draw_str
import serial

currX = 0.0
currY = 0.0

help_message = '''
USAGE: facedetect.py [--cascade <cascade_fn>]
'''

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(20, 20), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    # print "length of rects:", len(rects)
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def updatePos(img, rects):
    for x1, y1, x2, y2 in rects:
        global currX
        global currY
        ymax, xmax = img.shape[:2]
        currX = (x1 + x2) / 2.0
        currY = (y1 + y2) / 2.0
        currX /= xmax
        currY /= ymax
        currY = 1.0 - currY

if __name__ == '__main__':
    import sys, getopt, os, signal, time
    print help_message
    
    # FIXME
    # sername = '/dev/ttyAMA0'
    # ser = serial.Serial(sername, 9600)

    imfile = "/tmp/camcap.jpgi"

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade='])
    args = dict(args)
    cascade_fn = args.get('--cascade', "data/haarcascades/haarcascade_frontalface_default.xml")
    
    cascade = cv2.CascadeClassifier(cascade_fn)
    
    f = open("/tmp/raspifastcamd.pid")
    pid = int(f.readline())
    print "pid is: ", pid
    f.close()
    # if os.path.exists(imfile):
    #     os.remove(imfile)
    os.kill(pid, signal.SIGUSR1)
    time.sleep(1.0)
    x = 0
    lastfind = 0
    while True:
        time.sleep(0.2)
        lastfind += 1
        # print "reading"
        img = cv2.imread(imfile)
        os.kill(pid, signal.SIGUSR1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.equalizeHist(gray)

        t = clock()
        rects = detect(gray, cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))
        if len(rects) == 1:
            lastfind = 0
            # print "one object found"
            updatePos(img, rects)

        # if ser.inWaiting():
        x += 1
        if not x%2:
            # if ser.readline()[0] == '?':
            # ser.write("1 " if lastfind < 2 else "0 ")
            # ser.write("%.4f %.4f" % (currX, currY))
            # ser.write("\n")
            print ("1 " if lastfind < 2 else "0 ") + "%.4f %.4f" % (currX, currY)
        dt = clock() - t

        draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
        cv2.imshow('facedetect', vis)
        # time.sleep(0.3)

        if 0xFF & cv2.waitKey(5) == 27:
            break
    cv2.destroyAllWindows()

