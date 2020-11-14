import Motor
import time

class Controller:
    def controle(motor):
        while (True):
            val = input('スピードを入力（例 ”40, -30"）: ')
            val = val.split(',')
            motor.set_speed(val[0], val[1])
    
    def main():
        motor = Motor.Motor(18, 25, 24,13, 17, 27)
        motor.controle(50,50)
        
if __name__ == "__main__":
    Controller.main()
    GPIO.cleanup()