from flask import Flask, render_template, request

import time
import threading
import pigpio

gpio_pwm0 = 18
gpio_pin0 = 5
gpio_pin1 = 6
gpio_pwm1 = 19
gpio_pin2 = 13
gpio_pin3 = 26
gpio_serbo0 = 14
gpio_serbo1 = 15

pi = pigpio.pi()
pi.set_mode(gpio_pin0, pigpio.OUTPUT)
pi.set_mode(gpio_pin1, pigpio.OUTPUT)
pi.set_mode(gpio_pin2, pigpio.OUTPUT)
pi.set_mode(gpio_pin3, pigpio.OUTPUT)
pi.set_mode(gpio_pwm0, pigpio.OUTPUT)
pi.set_mode(gpio_pwm1, pigpio.OUTPUT)
pi.set_mode(gpio_serbo0, pigpio.OUTPUT)
pi.set_mode(gpio_serbo1, pigpio.OUTPUT)

pi.set_PWM_frequency(gpio_serbo0, 50)
pi.set_PWM_frequency(gpio_serbo1, 50)
pi.set_PWM_range(gpio_serbo0, 100)
pi.set_PWM_range(gpio_serbo1, 100)

app = Flask(__name__)

moter_effect = 10
now_left, now_right = 0,0
hz =20


def move(degree_x, degree_y):  
    pi.set_servo_pulsewidth(gpio_serbo0, degree_x)
    pi.set_servo_pulsewidth(gpio_serbo1, degree_y)
#     pi.set_PWM_dutycycle(gpio_serbo0, degree_x)
#     pi.set_PWM_dutycycle(gpio_serbo1, degree_y)
        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        res = request.form['get_key']
        if res == "up" :
            print("up")
            
            update_speed(90,90)
        elif res == "right" :
            print("right")
            
            update_speed(90,-90)
        elif res == "left" :
            print("left")
            
            update_speed(-90,90)
        elif res == "down" :
            while(1):
                print("11")
            print("down")
            update_speed(-90,-90)
        elif res == "stop":
            print("stop")
            update_speed(0,0, 30)
        return ('', 204)
    elif request.method == 'GET':
        return render_template('index.html')

def update_speed(left, right, degree = 0):
    global moter_effect
    if degree:
        moter_effect = degree
    if left - now_left > moter_effect/2:
        left_wheel(now_left + moter_effect)
    elif left - now_left < -moter_effect/2:
        left_wheel(now_left - moter_effect)
    else:
        left_wheel(left)
    
    
    if right - now_right > moter_effect/2:
        
        right_wheel(now_right + moter_effect)
    elif right - now_right < -moter_effect/2:
        right_wheel(now_right - moter_effect)
    else:
        right_wheel(right)
    moter_effect = 1
    print("left:{}, right:{}".format(now_left, now_right))
    
    
    
    
def left_wheel(left):
    global now_left
    
    now_left = left
    if left>=0:
        pi.write(gpio_pin0,1)
        pi.write(gpio_pin1,0)
        pi.hardware_PWM(gpio_pwm0, hz, left*10000)
        
    else:
        pi.write(gpio_pin0,0)
        pi.write(gpio_pin1,1)
        pi.hardware_PWM(gpio_pwm0, hz, -left*10000)

def right_wheel(right):
    global now_right
    
    now_right = right
    if right>=0:
        pi.write(gpio_pin2,0)
        pi.write(gpio_pin3,1)
        pi.hardware_PWM(gpio_pwm1, hz, right*10000)
    else:
        
        pi.write(gpio_pin2,1)
        pi.write(gpio_pin3,0)
        pi.hardware_PWM(gpio_pwm1, hz, -right*10000)
        

if __name__ == '__main__':
    
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded=True)
    pi.write(gpio_pin1,0)
    pi.write(gpio_pin2,0)
    pi.set_mode(gpio_serbo0, pigpio.INPUT)
    pi.set_mode(gpio_serbo1, pigpio.INPUT)
    pi.stop()
    print("Controll End")