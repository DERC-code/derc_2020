import cv2
import numpy as np
import time
import math
import threading
width=320
height=240
tile_num_x = 40
tile_num_y = int(tile_num_x*(3/4))
weight_map = np.zeros(tile_num_x*tile_num_y)
diff_frame = np.zeros((height, width))
weight_img = np.zeros((height,width), np.uint8)
sub_weight = 5


#アスペクト比４：３
#タイル内の描画ピクセル数で重み付け、大きなのノイズはタイルのサイズで調整
def main():
    tile_list = make_tile_list()
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)
    cap.set(4, 240)
    width = cap.get(3)
    height = cap.get(4)
    
    t1 = threading.Thread(target=pointer, args=(tile_list,))
    t1.setDaemon(True)
    t1.start()

    
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

def pointer(tile_list):
    global weight_img
    while(True):
        conditions = (diff_frame[:,:]>254)*1
        draw_weight(conditions, tile_list)
        weight_conditions = weight_map[:]>200
        #print(1)
        if np.sum(weight_conditions) > 0:
            #masked_tile_list = tile_list*weight_conditions
            sum_weight = np.sum(weight_conditions)
            masked_tile_list = [[tile_list[i][j]*weight_conditions[i] for j in range(0,4)] for i in range(0,len(tile_list))]

            circle_x = np.sum(np.array(masked_tile_list)[:,0:3:2]//2)//sum_weight
            circle_y = np.sum(np.array(masked_tile_list)[:,1:4:2]//2)//sum_weight
            #cv2.circle(weight_img, (circle_x, circle_y),15, (255,0,0), 2)
            print(circle_x, circle_y)
            #weight_img = np.zeros((height,width), np.uint8)

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

def draw_weight(conditions, tile_list):
    global weight_map
    weight_map -= sub_weight
    for i in range(tile_num_x*tile_num_y):
        weight_map[i] += int(np.sum(conditions[tile_list[i][1]:tile_list[i][3]+1,tile_list[i][0]:tile_list[i][2]+1]))
        if weight_map[i]>255:
            weight_map[i]=255
        elif weight_map[i]<0 :
            weight_map[i] = 0
        #cv2.rectangle(weight_img, (tile_list[i][0],tile_list[i][1]), (tile_list[i][2],tile_list[i][3]), weight_map[i], thickness=-1)
        
    
    
if __name__ == "__main__":
    print("start")
    main()

