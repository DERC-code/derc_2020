import serial
import micropyGPS
import threading
import time
import motor
import mpu92_forTest
import math
import numpy as np
import RPi.GPIO as GPIO

gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                     # 引数はタイムゾーンの時差と出力フォーマット
motor = motor.Motor(18, 25, 24,13, 17, 27)

def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s = serial.Serial('/dev/serial0', 9600, timeout=10)
    s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)

def get_gps():
    if gps.clean_sentences > 20:
        return (gps.latitude[0], gps.longitude[0])
    else:
        return None
       
    
def init():
    gpsthread = threading.Thread(target=rungps, args=()) # 上の関数を実行するスレッドを生成
    gpsthread.daemon = True
    gpsthread.start() # スレッドを起動

def rotation(x, t):
    a = np.array([[np.cos(t), -np.sin(t)],
                  [np.sin(t),  np.cos(t)]])
    ax = np.dot(a, x)        
    return ax

def calrad(target_x :float, target_y :float):
    myGps=get_gps()
    if myGps == None:
        return 0
    radT = math.atan2(target_x - myGps[0],target_y - myGps[1])
    magnet = mpu92_forTest.get_magnet()
    print(magnet[0]-25)
    print(magnet[1]-8)
#     x = magnet[0]
#     y = magnet[1]
    vr = np.array([magnet[0] -25,magnet[1] -8])
    rotated_vr = rotation(vr, -radT)
    rotated_rad = math.atan2(rotated_vr[1], rotated_vr[0])
    return rotated_rad
    
def main():
    init()
    mpu92_forTest.MPU9265_init()
    target_location_x= 34.805843
    target_location_y= 135.778176
    target_rad=0
    while True:
        target_rad = calrad(target_location_x,target_location_y)
        print("target_rad")
        print(target_rad * (180/np.pi))
        print()
        if target_rad >0.174533 :#0.174533=10度
            motor.set_speed(-100,100)
        elif target_rad < -0.174533:
            motor.set_speed(100,-100)
        else:
            pass
        time.sleep(1)
        
if __name__ == "__main__":
    main()
    