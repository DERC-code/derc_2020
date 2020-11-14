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
    
def main():
    #set up
    #センサーセットアップ
    init()
    mpu92_forTest.MPU9265_init()
    #目標をセット
    target_location_x= 34.805843
    target_location_y= 135.778176
    target_rad=0.0
    #roverの状態（フェーズ）
    phase = 0
    #move
    while True:
        if phase == 0:#x秒前進
            print("phase:0")
            motor.set_speed(100,100)
            time.sleep(5)#単位は秒
            phase = 1 #次のフェーズへ
        elif phase == 1:
            print("phase:1")
            if -0.001<(get_gps()[0]-target_location_x) and (get_gps()[0]-target_location_x)<0.001:# 緯度の差が0.01以内で
                if  -0.001<(get_gps()[1]-target_location_y) and (get_gps()[1]-target_location_y)<0.001:# かつ経度の差が0.01以内ならば
                    phase = 2 # 次のフェーズへ
                    continue
            target_rad = calrad(target_location_x,target_location_y,25,8)
            print(target_rad * (180/np.pi))
            if target_rad >0.174533 :#0.174533=10度
                print("左回転")#target_radを減らす方向
                motor.set_speed(50,100)
            elif target_rad < -0.174533:
                print("右回転")# target_radを増やす方向
                motor.set_speed(100,50)
            else:# -10度< Θ < 10度
                print("直進")
                motor.set_speed(100,100)
            time.sleep(1)
        elif phase ==2:#カメラモード
            print("phase:2")
            phase =3
        elif phase ==3:
            print("phase:3")
            break
    GPIO.cleanup()
    print("正常終了")
        
if __name__ == "__main__":
    main()
    