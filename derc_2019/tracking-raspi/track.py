#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pigpio
import time
pi = pigpio.pi()

X_MAX = 1500 #下向き
X_MIN = 800 #上向き
X_HOME = 1300
Y_MAX = 1700 #左向き
Y_MIN = 900 #右向き
Y_HOME = 1300

def move(degree_x, degree_y):
    duty_x = int((X_MAX-X_MIN )/100.0 * degree_x + X_HOME)
    duty_y = int((Y_MAX-Y_MIN)/100.0 * degree_y + Y_HOME)   
    pi.set_servo_pulsewidth(4, duty_x)
    pi.set_servo_pulsewidth(17, duty_y)

def main():


if __name__ == '__main__':
    main()