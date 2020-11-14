import serial
import micropyGPS
import threading
import time
import motor
import mpu92_forTest
import math
import numpy as np
import RPi.GPIO as GPIO
import ta7291
import sys

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

'''
calrad 自身の方向ベクトルと自身から目標へのベクトルのなす角を計算
@param {float} target_x, target_y :目標のｘ（緯度）、ｙ（経度）
@param {float} fix_x, fix_y : 地磁気センサの修正値（ｘ、ｙ）
@return {float} rotated_rad : 自身の方向ベクトルと自身から目標へのベクトルのなす角(rad)
'''
def calrad(target_x :float, target_y :float, fix_x :float, fix_y :float):
    myGps=get_gps()
    if myGps == None:
        return 0.0
    radT = math.atan2(target_x - myGps[0],target_y - myGps[1])
    magnet = mpu92_forTest.get_magnet()
    vr = np.array([magnet[0] - fix_x,magnet[1] -fix_y])
    rotated_vr = rotation(vr, -radT)
    rotated_rad = math.atan2(rotated_vr[1], rotated_vr[0])
    return rotated_rad

maxX = -10000
maxY = -10000
minX = 10000
minY = 10000

def calc():
    global maxX
    global minX
    global maxY
    global minY

    t_end = time.time() + 30
    setspeed = 80
    #motor = Motor.Motor(18, 25, 24,13, 27, 17)
    #time.sleep(5)
    while time.time() < t_end:     
        magnet = mpu92_forTest.get_magnet()
        print(magnet)
        if(maxX < magnet[0]):
            maxX = magnet[0]
        if(minX > magnet[0]):
            minX = magnet[0]
        if(maxY < magnet[1]):
            maxY = magnet[1]
        if(minY > magnet[1]):
            minY = magnet[1]
#         print("maxx",maxX)
#         print("minx",minX)
#         print()
#         print("maxy",maxY)
#         print("miny",minY)
#         print()
        motor.set_speed(-setspeed,setspeed) 
        time.sleep(1) 


def get_cecter_x(maxX,minX):
    center_x = (maxX + minX)/ 2
    return center_x

def get_cecter_y(maxY,minY):
    center_y = (maxY + minY)/ 2
    return center_y
    

def main():
    #set up
    #センサーセットアップ
    init()
    mpu92_forTest.MPU9265_init()
    #目標をセット
    target_location_x = 34.805843
    target_location_y = 135.778176
    target_rad=0.0
    #中心
    calc()
    center_x = get_cecter_x(maxX,minX)
    center_y = get_cecter_y(maxY,minY)
    print(center_x)
    print(center_y)
    #roverの状態（フェーズ）
    phase = 0
    #move
    while True:
        pass
    
if __name__ == "__main__":
    main()
    