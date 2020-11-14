import mpu92_test
import time

class mag():
    def __init__(self):
        self.mag_x=0.0
        self.mag_y=0.0
        
    def calcenter(self,maxX,minX,maxY,minY):
        self.center_x = (maxX + minX)/2.0
        self.center_y = (maxY + minY)/2.0
    
    def main():
        magnet = mpu92_test.get_magnet();
        mag = mag()
        mag.calcenter(42.0,-5.0,38.0,-10.0)
        mag.mag_x = magnet[0] + self.center_x
        mag.mag_y = magnet[1] + self.center_y
        print(instance.mag_x)
        print(instance.mag_y)
        while True:
            magnet = mpu92_test.get_magnet();
            self.mag_x = magnet[0] + self.center_x
            self.mag_y = magnet[1] + self.center_y
            print(self.mag_x)
            print(self.mag_y)
            time.sleep(0.1)

if __name__ == "__main__":
    mag = mag()
    mag.main()