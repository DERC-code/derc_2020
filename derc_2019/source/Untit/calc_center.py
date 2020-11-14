import mpu92_test
import time

def main():
    
    maxX = -100
    maxY = -100
    minX = 100
    minY = 100
    
    while True:
        magnet = mpu92_test.get_magnet()
        
        if(maxX < magnet[0]):
            maxX = magnet[0]
        if(minX > magnet[0]):
            minX = magnet[0]
        if(maxY < magnet[1]):
            maxY = magnet[1]
        if(minY > magnet[1]):
            minY = magnet[1]
            
        #print("magnet[%+4.2f, %+4.2f, %+4.2f]" % (magnet[0], magnet[1], magnet[2]), end="\t")
        
        print("maxx",maxX)
        print("minx",minX)
        print()
        print("maxy",maxY)
        print("miny",minY)
        print()
        
        time.sleep(1)
        
if __name__ == '__main__':
    main()