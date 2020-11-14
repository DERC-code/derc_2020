#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import serial
import time
import threading

ser = serial.Serial('/dev/ttyUSB0',115200,timeout=None)
flag = True

def moter():
	while(flag):
		
		
		ser.write(str.encode('m0:40\n'))
		ser.write(str.encode('m1:40\n'))
		time.sleep(3)
		ser.write(str.encode('m0:-100\n'))
		ser.write(str.encode('m1:-100\n'))
		time.sleep(3)
    

def main():
	th = threading.Thread(target=moter)
	th.setDaemon(True)
	th.start()

	global flag
	input()
	flag = False
	

	ser.write(str.encode('m0:0\n'))
	ser.write(str.encode('m1:0\n'))
	ser.close() 

if __name__ == "__main__":
    print("start")
    main()


