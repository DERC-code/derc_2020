# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import pigpio
import VL53L0X 
import threading

gpio_pwm0 = 18
gpio_pin0 = 5
gpio_pin1 = 6
gpio_pwm1 = 19
gpio_pin2 = 13
gpio_pin3 = 26
gpio_serbo0 = 14
gpio_serbo1 = 15

pi = pigpio.pi()
pi.set_mode(gpio_pin0, pigpio.OUTPUT)
pi.set_mode(gpio_pin1, pigpio.OUTPUT)
pi.set_mode(gpio_pin2, pigpio.OUTPUT)
pi.set_mode(gpio_pin3, pigpio.OUTPUT)
pi.set_mode(gpio_pwm0, pigpio.OUTPUT)
pi.set_mode(gpio_pwm1, pigpio.OUTPUT)
pi.set_mode(gpio_serbo0, pigpio.OUTPUT)
pi.set_mode(gpio_serbo1, pigpio.OUTPUT)

pi.set_PWM_frequency(gpio_serbo0, 50)
pi.set_PWM_frequency(gpio_serbo1, 50)
pi.set_PWM_range(gpio_serbo0, 100)
pi.set_PWM_range(gpio_serbo1, 100)

stop_flag = False
back_flag = False
now_degree_x,now_degree_y = 1300,1300
serbo_effect = 0.4
moter_effect = 5
moter_effect2 = 0.2

now_left, now_right = 0,0
hz =20


def approach():
    diff =   now_degree_x - 1300
    if diff <-50:
        update_speed(-diff*moter_effect2,diff*moter_effect2)
    elif diff >50:
        update_speed(-diff*moter_effect2,diff*moter_effect2)
  
    else:
        update_speed(20,20, degree = 30)
        
def update_speed(left, right, degree = 0):
    global moter_effect
    if degree:
        moter_effect = degree
    if left - now_left > moter_effect/2:
        left_wheel(now_left + moter_effect)
    elif left - now_left < -moter_effect/2:
        left_wheel(now_left - moter_effect)
    else:
        left_wheel(left)
    
    
    if right - now_right > moter_effect/2:
        
        right_wheel(now_right + moter_effect)
    elif right - now_right < -moter_effect/2:
        right_wheel(now_right - moter_effect)
    else:
        right_wheel(right)
    moter_effect = 1
    print("left:{}, right:{}".format(now_left, now_right))
    
def set_speed( left, right):
    left_wheel(left)
    right_wheel(right)
    print("left:{}, right:{}".format(now_left, now_right))
    
    
def left_wheel(left):
    global now_left
    left = int(left)
    if left>90:
        left = 90
    
    now_left = left
    if left>=0:
        pi.write(gpio_pin0,1)
        pi.write(gpio_pin1,0)
        pi.hardware_PWM(gpio_pwm0, hz, left*10000)
        
    else:
        pi.write(gpio_pin0,0)
        pi.write(gpio_pin1,1)
        pi.hardware_PWM(gpio_pwm0, hz, -left*10000)

def right_wheel(right):
    global now_right
    right = int(right)
    if right>90:
        right = 90
    now_right = right
    if right>=0:
        pi.write(gpio_pin2,0)
        pi.write(gpio_pin3,1)
        pi.hardware_PWM(gpio_pwm1, hz, right*10000)
    else:
        
        pi.write(gpio_pin2,1)
        pi.write(gpio_pin3,0)
        pi.hardware_PWM(gpio_pwm1, hz, -right*10000)
def get_distance():
    tof = VL53L0X.VL53L0X(address=0x29)
    global back_flag, stop_flag
    #距離の取得を開始する
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    try:
        while True:
            dist = tof.get_distance()	 #VL53L0Xから距離[mm]を取得する
            
            if dist != 0:
                if dist <100:
                    print("emergency!!")
                    back_flag = True
                elif dist >100 and dist<150:
                    stop_flag = True
                #print ("%d mm " % dist)	 #距離[cm]を表示する
                time.sleep(0.2)              #1[s]スリープする
    except KeyboardInterrupt  :        	 #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
    except Exception as e:
        print(str(e))                   #例外処理の内容をコンソールに表示
    finally:
        tof.stop_ranging()              #VL53L0Xの終了処理
        print("\nexit program")  
    
def move(degree_x, degree_y):  
    global now_degree_x,now_degree_y
    now_degree_x, now_degree_y = degree_x, degree_y
    
    pi.set_servo_pulsewidth(gpio_serbo1, degree_x)
    pi.set_servo_pulsewidth(gpio_serbo0, degree_y)
    
def main():
    t1 = threading.Thread(target=get_distance)
    t1.setDaemon(True)
    t1.start()
        # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
    args = vars(ap.parse_args())

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    redLower = (0, 70, 50)
    redUpper = (10, 255, 255)

    redLower2 = (170, 70, 50)
    redUpper2 = (180, 255, 255)

    greenLower = (60, 77, 50)
    greenUpper = (90, 255, 100)

    yellowLower = (25, 85, 90)
    yellowUpper = (35, 255, 255)
    #https://webllica.com/cmyk-rgb-hsl-hsv-hex-color-code-calculator/
    pts = deque(maxlen=args["buffer"])

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        vs = VideoStream(src=0).start()

    # otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(args["video"])

    # allow the camera or video file to warm up
    time.sleep(2.0)

    # keep looping
    while True:
        # grab the current frame
        frame = vs.read()

        # handle the frame from VideoCapture or VideoStream
        frame = frame[1] if args.get("video", False) else frame

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break

        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=400)
        
        size = (frame.shape[1], frame.shape[0])
        
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask

        mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    
        #mask = cv2.bitwise_or(mask1, mask2)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

           # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)


            # only proceed if the radius meets a minimum size
            if radius > 15:
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)

        # update the points queue


       # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        #-------------------サーボ、モーター制御-------------------------------------
        global back_flag, stop_flag
        if back_flag:
            update_speed(-20,-20, degree = 40)
        if stop_flag:
            update_speed(0,0, degree = 40)
        elif center:
            search(center, size)
            approach()
        else:
            update_speed(0,0)
        stop_flag = False
        back_flag = False
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

       
        if key == ord("q"):
            break

    # if we are not using a video file, stop the camera video stream
    if not args.get("video", False):
        vs.stop()

    # otherwise, release the camera
    else:
        vs.release()

    # close all windows
    cv2.destroyAllWindows()
    pi.hardware_PWM(gpio_pwm1, hz, 0)
    pi.hardware_PWM(gpio_pwm0, hz, 0)
    
def search(center, size):
    
    move_degree_x = now_degree_x  - (center[0]-size[0]/2)*serbo_effect #x
    move_degree_y = now_degree_y + (center[1]-size[1]/2)*serbo_effect #y
    move(move_degree_x, move_degree_y)
    
if __name__ == "__main__":
    print("start")
    pi.set_servo_pulsewidth(gpio_serbo0, 1300)
    pi.set_servo_pulsewidth(gpio_serbo1, 1300)
    main()
