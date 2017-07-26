#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests the various feature detector algorithms in OpenCV 2.4 on one image

@SINCE: Thu Sep 13 23:01:23 2012
@VERSION: 0.1

@REQUIRES: OpenCV 2.4 (I used 2.4.0), matplotlib

@AUTHOR: Ripley6811
@ORGANIZATION: National Cheng Kung University, Department of Earth Sciences
"""
__author__ = 'Ripley6811'
__copyright__ = ''
__license__ = ''
__date__ = 'Thu Sep 13 23:01:23 2012'
__version__ = '0.1'



import matplotlib.pyplot as plt  # plt.plot(x,y)  plt.show()
import cv2
import time



def test_feature_detector(detector, imfname):
    image = cv2.imread(imfname)
    forb = cv2.FeatureDetector_create(detector)
    # Detect crashes program if image is not greyscale
    t1 = time.time()
    kpts = forb.detect(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    t2 = time.time()
    print detector, 'number of KeyPoint objects', len(kpts), '(time', t2-t1, ')'

    return kpts


def main():
    imfname = r'_______.bmp'


    detector_format = ["","Grid","Pyramid"]
    # "Dense" and "SimpleBlob" omitted because they caused the program to crash
    detector_types = ["FAST","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"]


    for form in detector_format:
        for detector in detector_types:
            kpts = test_feature_detector(form + detector, imfname)

            # KeyPoint class: angle, class_id, octave, pt, response, size
            plt.figure(form + detector)
            for k in kpts:
                x,y = k.pt
                plt.plot(x,-y,'ro')
            plt.axis('equal')

    plt.show()


if __name__ == '__main__':
    main()
