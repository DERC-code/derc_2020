#!/usr/bin/python
# -*- coding: utf-8 -*-


import cv2
import numpy as np

print(cv2.__version__)

def color_detect(img):
    # Translating into HSV space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # A threshold of the target: blue
    hsv_min = np.array([95,190,140])
    hsv_max = np.array([110,255,255])

    # A threshold of the target: orange
    #hsv_min = np.array([15,120,125])
    #hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    return mask1


def main():
    # Capturing the image of camera
    cap = cv2.VideoCapture(0)
    ret = cap.set(3, 640)
    ret = cap.set(4, 480)
    
    while(cap.isOpened()):
        # Getting a frame
        ret, frame = cap.read()

        # Detecting the target
        mask = color_detect(frame)

        # Drawing the contours and the rect bounded
        contours, hierarchy  = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        for contour in contours:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            rects.append(np.array(rect))

        # Grasping the target
        if len(rects) > 0:
            rect = max(rects, key=(lambda x: x[2] * x[3]))
            if rect[2] * rect[3] > 30:    
                cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=2)
                (xX, yY) = tuple(rect[0:2] + rect[2:4] / 2)
                cv2.line(frame,(xX,0),(xX,479),(255,255,0),3)
                cv2.line(frame,(0,yY),(639,yY),(255,255,0),3)
            
                # Print the position information
                fontType = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, str(tuple(rect[0:2])), (rect[0]-40, rect[1]-15), fontType, 1, (0, 0, 255), 2, cv2.CV_AA)
                print(rect[0], rect[1], rect[2], rect[3])
            
        # Showing the final image
        cv2.imshow("Frame", frame)

        # Press 'q' to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()