import serial
import micropyGPS
import threading
import time
import motor


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
    
def main():
    init()
    n=0
    while True:
        n = n+1
        time.sleep(1)
        #motor.set_speed(n%90,n%90)
        motor.set_speed(100,100)
        print(get_gps())
        
if __name__ == "__main__":
    main()
    