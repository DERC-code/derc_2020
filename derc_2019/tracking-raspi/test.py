
#!/usr/bin/python
# -*- coding: utf-8 -*-
import pigpio
import time
pi = pigpio.pi()
#x_move:range720-2370
#y_move:range1000-2315
def move(x_move, y_move):
    print('x_move: ', x_move)
    print('y_move: ', y_move)
    pi.set_servo_pulsewidth(4, x_move)
    pi.set_servo_pulsewidth(17, y_move)
 

X_MAX = 1500 #下向き
X_MIN = 800　#上向き
X_HOME = 1300
 
Y_MAX = 1700 #左向き
Y_MIN = 900 #右向き
Y_HOME = 1300
 
if __name__ == '__main__':
    print("Aaaa")
    move(X_HOME, Y_HOME)
    time.sleep(2)
    move(X_MIN, Y_HOME)
    time.sleep(2)
    move(X_MAX, Y_HOME)
    time.sleep(2)
    move(X_HOME, Y_HOME)
    time.sleep(2)
    move(X_HOME, Y_MIN)
    time.sleep(2)
    move(X_HOME, Y_MAX)
    time.sleep(2)
    move(X_HOME, Y_HOME)