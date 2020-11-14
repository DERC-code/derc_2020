# -*- coding: utf-8 -*-
import smbus
from time import sleep
import numpy as np
 
MPU9265 = 0x68
AK8963 = 0x0c
bus = smbus.SMBus(1)
 
def main():
    MPU9265_init()
 
    while True:
        gyro = get_gyro()
        accel = get_accel()
        magnet = get_magnet()
        temp = get_temp()
 
        print("gyro[%+4.2f, %+4.2f, %+4.2f]" % (gyro[0], gyro[1], gyro[2]), end="\t")
        print("accel[%+4.2f, %+4.2f, %+4.2f]" % (accel[0], accel[1], accel[2]), end="\t")
        print("magnet[%+4.2f, %+4.2f, %+4.2f]" % (magnet[0], magnet[1], magnet[2]), end="\t")
        print("temp[%+4.2f]" % (temp))
        sleep(0.1)

def MPU9265_init():
    # スリープモードの解除
    bus.write_i2c_block_data(MPU9265, 0x6B, [0x00])
    sleep(0.01)
 
    # 加速度センサの起動
    bus.write_i2c_block_data(MPU9265, 0x37, [0x02])
    sleep(0.01)
 
    # 地磁気センサの起動
    bus.write_i2c_block_data(MPU9265, 0x37, [0x02])
    sleep(0.01)
 
    # ±16gに設定
    bus.write_i2c_block_data(MPU9265, 0x1B, [0x18])
    sleep(0.01)
 
    # ±16gに設定
    bus.write_i2c_block_data(MPU9265, 0x1C, [0x18])
    sleep(0.01)
 
    # 取得周期100Hzに設定
    bus.write_i2c_block_data(AK8963, 0x0A, [0x16])
    sleep(0.01)

def get_gyro():
    gyro = []
    data = bus.read_i2c_block_data(MPU9265, 0x43, 6)
    gyro.append(u2s(data[0] << 8 | data[1]) / float(0x8000) * 16.0)
    gyro.append(u2s(data[2] << 8 | data[3]) / float(0x8000) * 16.0)
    gyro.append(u2s(data[4] << 8 | data[5]) / float(0x8000) * 16.0)
 
    return gyro
 
def get_accel():
    accel = []
    data = bus.read_i2c_block_data(MPU9265, 0x3B, 6)
    accel.append(u2s(data[0] << 8 | data[1]) / float(0x8000) * 16.0)
    accel.append(u2s(data[2] << 8 | data[3]) / float(0x8000) * 16.0)
    accel.append(u2s(data[4] << 8 | data[5]) / float(0x8000) * 16.0)
 
    return accel
 
def get_magnet():
    magnet = []
    flag = bus.read_i2c_block_data(AK8963, 0x02, 1)
    if flag[0] & 1:
        data = bus.read_i2c_block_data(AK8963, 0x03, 7)
        magnet.append(u2s(data[3] << 8 | data[2]) / float(0x8000) * 4800.0)
        magnet.append(u2s(data[1] << 8 | data[0]) / float(0x8000) * 4800.0)
        magnet.append(u2s(data[5] << 8 | data[4]) / float(0x8000) * 4800.0)
    else:
        return np.array([np.nan, np.nan, np.nan])
 
    return magnet
 
def get_temp():
    data = bus.read_i2c_block_data(MPU9265, 0x41, 2)
    temp_raw = u2s(data[0] << 8 | data[1])
    temp = ((temp_raw - 0.0) / 333.87) + 21.0
 
    return temp
 
# unsignedをsigned(符号付)に変換
def u2s(x):
    if x & (0x01 << 15):
        return -1 * ((x ^ 0xffff) + 1)
    else:
        return x

if __name__ == '__main__':
    main()