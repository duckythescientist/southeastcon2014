import numpy as np
import cv2
import cv2.cv as cv
import sys, os, signal, time
from common import clock, draw_str

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        # cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        print (x1 + x2) / 2.0 + x1,
        print (y1 + y2) / 2.0 + y1

if len(sys.argv) != 3:
	print "usage: python programname.py cascade img"
casfile = sys.argv[1]
imfile = sys.argv[2]

cascade = cv2.CascadeClassifier(casfile)

img = cv2.imread(imfile)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.equalizeHist(gray)

t = clock()
rects = detect(gray, cascade)
vis = img.copy()
draw_rects(vis, rects, (0, 255, 0))

# dt = clock() - t

# draw_str(vis, (20, 20), 'time: %.1f ms' % (dt*1000))
# cv2.imshow('facedetect', vis)
# time.sleep(0.3)

# raw_input()


