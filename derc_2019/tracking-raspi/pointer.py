#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import subprocess
import time
import RPi.GPIO as GPIO

print(cv2.__version__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

panX = 90 * 8 # The coefficient 8 is chosen to get a good unit for counting. 
tiltY = 90 * 8
recDD = np.array([0,0])
recTime = time.time()
recTime2 = time.time()
autoTrack = True
dX = 0
dY = 0

def color_detect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # For Target Blue
    #hsv_min = np.array([95,190,140])
    #hsv_max = np.array([110,255,255])

    # For Target Orange (an alternative)
    #hsv_min = np.array([15,120,125])
    #hsv_max = np.array([30,255,255])

    # For Target Orange
    hsv_min = np.array([15,80,200])
    hsv_max = np.array([33,245,255])
    
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    return mask1


def main():
    cap = cv2.VideoCapture(0)
    ret = cap.set(3, 320)
    ret = cap.set(4, 240)
    
    while(cap.isOpened()):
        
        global panX 
        global tiltY
        global autoTrack
        global dX 
        global dY
        global recTime2

        # Set the camera to face forward when starting autonomous tracing and pointing
        if GPIO.input(5)==0 and autoTrack==False:
            cmd = 'python /home/pi/adx_PR3_uart180.py -20790'
            subprocess.Popen(cmd, shell=True)
            # Send twice to pass through a error filter in Arduino
            time.sleep(0.02)
            subprocess.Popen(cmd, shell=True)

            time.sleep(0.2)
            recTime2 = time.time()
            autoTrack = True
            # Face forward: 20790 = 115*180 + 90
            panX = 115 * 8
            tiltY = 90 * 8
        elif GPIO.input(5)==1 and autoTrack==True:
            autoTrack = False

        ret, frame = cap.read()
        mask = color_detect(frame)
        contours, hierarchy  = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rects = []
        for contour in contours:
            approx = cv2.convexHull(contour)
            rect = cv2.boundingRect(approx)
            rects.append(np.array(rect))
        if len(rects) > 0:
            rect = max(rects, key=(lambda x: x[2] * x[3]))
            if rect[2] * rect[3] > 30:    
                global recDD
                global recTime
                recPX = panX
                recTY = tiltY
                dX = (rect[0] + rect[2] / 2) - 160
                dY = (rect[1] + rect[3] / 2) - 120
                if (abs(dX) > 25) or (abs(dY) > 25):
                    recDD = [dX,dY]

                denomiScale = 65
                if abs(dX) > 25:
                    panX = panX - dX * 10 / denomiScale
                    if panX > 179 * 8:
                        panX = 179 * 8
                    elif panX < 8:
                        panX = 8
                if abs(dY) > 18:
                    tiltY = tiltY - dY * 10 / denomiScale
                    if tiltY > 179 * 8:
                        tiltY = 179 * 8
                    elif tiltY < 8:
                        tiltY = 8                
                
                # Continue watching the target
                if (not recPX == panX) or (not recTY == tiltY):
                    cmd = 'sudo python /home/pi/adx_PR3_uart180.py ' + str(-int(panX / 8) * 180 - int(tiltY / 8) * 1)
                    aaa = str(panX / 8) + ', ' + str(tiltY / 8)
                    subprocess.Popen(cmd, shell=True)

                    # Print position information
                    fontType = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, aaa, tuple(rect[0:2]), fontType, 1, (0, 0, 255), 2, cv2.CV_AA)

                    recTime = time.time()

                    # Continue facing the target
                    if autoTrack == 1:
                        # "tiltY" tells the horizontal information because the camera is attached vertically (in portrait mode).
                        if tiltY < 80 * 8:
                            nose = 9 * 180
                        elif tiltY > 100 * 8:
                            nose = 10 * 180
                        else:
                            nose = 3 * 180

                        speed = abs(tiltY / 8 - 90)
                        if speed > 15:
                            speed = 15
                        speed = int(speed * 70 / 15)  # The muximum PWM value is set 255*70/180 to reduce the noise of gearbox.                    
                        cmd = 'sudo python /home/pi/adx_PR3_uart180.py ' + str(nose + speed)
                        subprocess.Popen(cmd, shell=True)
                        print(tiltY / 8, panX / 8)

                elif rect[2] * rect[3] < 8000 and autoTrack == 1 and time.time()-recTime2 > 1.0:
                    cmd = 'sudo python /home/pi/adx_PR3_uart180.py 440'
                    subprocess.Popen(cmd, shell=True)
                elif rect[2] * rect[3] > 11000 and autoTrack == 1 and time.time()-recTime2 > 1.0:
                    cmd = 'sudo python /home/pi/adx_PR3_uart180.py 800'
                    subprocess.Popen(cmd, shell=True)

                cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=2)
                (xX, yY) = tuple(rect[0:2] + rect[2:4] / 2)
                cv2.line(frame,(xX,0),(xX,239),(255,255,0),3)
                cv2.line(frame,(0,yY),(319,yY),(255,255,0),3)

        # Follow the target for 1.2 sesonds when it goes out of sight of camera.
        elif time.time() - recTime < 1.2:
            denomiScale = 65
            panX = panX - dX * 10 / denomiScale
            if panX > 179 * 8:
                panX = 179 * 8
            elif panX < 8:
                panX = 8
            tiltY = tiltY - dY * 10 / denomiScale
            if tiltY > 179 * 8:
                tiltY = 179 * 8
            elif tiltY < 8:
                tiltY = 8
            print('aa ', tiltY / 8, panX / 8)
            cmd = 'sudo python /home/pi/adx_PR3_uart180.py ' + str(-int(panX / 8) * 180 - int(tiltY / 8) * 1)
            subprocess.Popen(cmd, shell=True)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()