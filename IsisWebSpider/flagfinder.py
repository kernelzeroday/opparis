#!/usr/bin/python

######  #         ##     ####   ######     #    #    #  #####   ######  #####
#       #        #  #   #    #  #          #    ##   #  #    #  #       #    #
#####   #       #    #  #       #####      #    # #  #  #    #  #####   #    #
#       #       ######  #  ###  #          #    #  # #  #    #  #       #####
#       #       #    #  #    #  #          #    #   ##  #    #  #       #   #
#       ######  #    #   ####   #          #    #    #  #####   ######  #    #

#
# quick n dirty based on the idea/program from munona and in code i found on the net, and ported to python by beta
# use the cascade file from flagfinder2.
# If someone interested in work on another cascade sheet and train it, contact me. Im beta
#
# The program accepts jpg input files list and display if has isis flags or not
# feel free to incorporate and modify it on your scripts #opparis
#

import cv2, sys
from cv2 import cv

def detect(img, cascade):
    for scale in [float(i)/10 for i in range(11, 15)]:
        for neighbors in range(2,5):
            rects = cascade.detectMultiScale(img, scaleFactor=scale, minNeighbors=neighbors,
                                             minSize=(10, 10), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

            if len(rects)>0:
	        return True
    return False

def loadCascadeFile():
    cascade_fn = "cascade.xml"
    cascade = cv2.CascadeClassifier(cascade_fn)
    return cascade

def find_flag(fname, cascade):
    try:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        detected = detect(gray, cascade)
        return detected
    except Exception as e:
        return False

if __name__ == '__main__':

    cascade=loadCascadeFile()
    for fname in sys.argv[1:]:
        print " %s %s " %  (fname, "isis" if find_flag(img) else "?")
