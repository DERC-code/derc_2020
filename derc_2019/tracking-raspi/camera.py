#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
print(cv2.__version__)
cap = cv2.VideoCapture(0)

while( cap.isOpened() ):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))    
    cv2.imshow('Capture',frame)
    key = cv2.waitKey(1)
    if key & 0x00FF  == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

