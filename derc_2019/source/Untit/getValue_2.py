import mpu92_test
import time

center_x = (42.0 + -5.0)/2.0
center_y = (38.0 + -10.0)/2.0
magnet = mpu92_test.get_magnet();
print(magnet[0]+center_x)
print(magnet[1]+center_y)
while True:
    magnet = mpu92_test.get_magnet();
    print(magnet[0]+center_x)
    print()
    print(magnet[1]+center_y)
    time.sleep(1)