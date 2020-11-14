import cv2
import numpy as np
import time
import math
import threading
import pigpio
import serial

pi = pigpio.pi()
ser = serial.Serial('/dev/ttyUSB0',115200,timeout=None)

X_MAX = 1700 #→
X_MIN = 900 #←
X_HOME = 1300
Y_MAX =  1500#下
Y_MIN =  800#上
Y_HOME = 900 

width=240
height=160

mean_x,mean_y = -1,-1
tile_num_x = 52
tile_num_y = int(tile_num_x*(3/4))
weight_map = np.zeros(tile_num_x*tile_num_y)
diff_frame = np.zeros((height, width))
weight_img = np.zeros((height,width), np.uint8)
sub_weight = 4



#アスペクト比４：３
#タイル内の描画ピクセル数で重み付け、大きなのノイズはタイルのサイズで調整
def main():
    global width,height
    
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    width = cap.get(3)
    height = cap.get(4)
    
    t1 = threading.Thread(target=search_point)
    #t2 = threading.Thread(target=track)
    t1.setDaemon(True)
    #t2.setDaemon(True)
    t1.start()
    #t2.start()

    
    global diff_frame
    _, frame = cap.read()
    while(True):
        
        _, next_frame =  cap.read()
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        diff_frame = fgbg.apply(frame)
        diff_frame = fgbg.apply(next_frame)
        frame = next_frame
        
        cv2.imshow('diff_frame',diff_frame)
        #cv2.imshow('frame', frame)
        #cv2.imshow('weight_map',weight_img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    
    cv2.destroyAllWindows()
#トラックするときはサーチしない、ポイントが中央にある場合はトラックしない

def search_point():
    now_degree_x, now_degree_y, move_degree_x, move_degree_y = X_HOME,Y_HOME,0,0
    move(X_HOME,Y_HOME)
    n=0
    global mean_x, mean_y
    global weight_img

    
    while(1):
        while(True):
            conditions = (diff_frame[:,:]>254)*1
            draw_weight(conditions)
            weight_conditions = weight_map[:]>200
            #print(1)
            if np.sum(weight_conditions) > 0:
                #masked_tile_list = tile_list*weight_conditions
                sum_weight = np.sum(weight_conditions)
                masked_tile_list = [[tile_list[i][j]*weight_conditions[i] for j in range(0,4)] for i in range(0,len(tile_list))]
                mean_x = np.sum(np.array(masked_tile_list)[:,0:3:2]//2)//sum_weight
                mean_y = np.sum(np.array(masked_tile_list)[:,1:4:2]//2)//sum_weight
                #cv2.circle(weight_img, (mean_x, mean_y),15, (255,0,0), 2)
                dX = mean_x - width/2
                dY = mean_y - height/2
                if (abs(dX) > 25) or (abs(dY) > 25):
                    
                    print("mx:{}, my:{}".format(move_degree_x,move_degree_y))
                    move_degree_x = int(now_degree_x - (mean_x-width/2)*0.3) #240/2
                    move_degree_y = int(now_degree_y + (mean_y-height/2)*0.3) #160/2
                    #print("{},{},{},{},{},{}".format(mean_x,mean_y,(mean_x-width/2),(mean_y-height/2), width, height))
                    move(move_degree_x, move_degree_y)
                    now_degree_x = move_degree_x
                    now_degree_y = move_degree_y
                #weight_img = np.zeros((height,width), np.uint8)
                else:
                    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    break
            else:
                mean_x, mean_y = -1,-1
            n = n + 1
            print("{}: 座標({},{})".format(n,mean_x, mean_y))

        if(1250 < now_degree_x and now_degree_x<1350):
            run(100,100)
        if(1100 < now_degree_x and now_degree_x <1500):
            if(now_degree_x-1300<0):
                run(80,70)
            else:
                run(70,80)
        else:
            if(now_degree_x-1300<0):
                run(90,70)
            else:
                run(70,90)
        time.sleep(1)
        run(0,0)
    
def run(left, right):
	text_left = 'm1:{}\n'.format(-left)
	text_right = 'm0:{}\n'.format(-right)
	ser.write(str.encode(text_left))
	ser.write(str.encode(text_right))

def make_tile_list():
    '''
    targetを分割し、そのリストを返します
    tile_numは分割数であり、第一引数がｘ軸方向、第二引数がｙ軸方向
    '''
    
    tile_list = []
    for y in range(0, tile_num_y):
        for x in range(0, tile_num_x):
            tile = (x*width/tile_num_x, y*height/tile_num_y,(x+1)*width/tile_num_x-1, (y+1)*height/tile_num_y-1 )
            tile = tuple(math.floor(i) for i in tile)
            tile_list.append(tile)
    return tile_list

def draw_weight(conditions):
    global weight_map
    weight_map -= sub_weight
    for i in range(tile_num_x*tile_num_y):
        weight_map[i] += int(np.sum(conditions[tile_list[i][1]:tile_list[i][3]+1,tile_list[i][0]:tile_list[i][2]+1]))
        if weight_map[i]>255:
            weight_map[i]=255
        elif weight_map[i]<0 :
            weight_map[i] = 0
        #cv2.rectangle(weight_img, (tile_list[i][0],tile_list[i][1]), (tile_list[i][2],tile_list[i][3]), weight_map[i], thickness=-1)
        
    
def move(degree_x, degree_y):  
    pi.set_servo_pulsewidth(4, degree_x)
    pi.set_servo_pulsewidth(17, degree_y)
 
if __name__ == "__main__":
    print("start")
    
    tile_list = make_tile_list()
    main()

