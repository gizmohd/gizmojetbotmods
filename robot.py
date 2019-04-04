from time import sleep
import traitlets
from traitlets.config.configurable import SingletonConfigurable
from adafruit_motorkit import MotorKit
kit = MotorKit(0x40)

sleep_time = 0.05

class Robot(SingletonConfigurable):
    
    left_motor = kit.motor2 
    right_motor = kit.motor1
    # config
    
    def __init__(self, *args, **kwargs):
        self.left_motor = kit.motor2 
        sleep(sleep_time)
        self.right_motor =kit.motor1

    def set_min_max(self, speed):
        if (speed == 0):
           return speed
        elif (speed > 1):
           return 1
        elif (speed < -1):
           return -1
        elif (speed > 0):
           return  0.3 + (speed * .7)
        else:
           return  -0.3 - (speed * .7)

    def set_motors(self, left_speed, right_speed):
        self.left_motor.throttle = self.set_min_max(left_speed)
        sleep(sleep_time)
        self.right_motor.throttle = self.set_min_max(right_speed)

    def forward(self, speed=1.0, duration=None):
        self.left_motor.throttle = self.set_min_max(speed)
        sleep(sleep_time)
        self.right_motor.throttle = self.set_min_max(speed)

    def backward(self, speed=1.0):
        self.left_motor.throttle = self.set_min_max(-speed)
        sleep(sleep_time) 
        self.right_motor.throttle = self.set_min_max(-speed)

    def left(self, speed=1.0):
        self.left_motor.throttle = self.set_min_max(-speed)
        sleep(sleep_time)
        self.right_motor.throttle = self.set_min_max(speed)

    def right(self, speed=1.0):
        self.left_motor.throttle = self.set_min_max(speed)
        sleep(sleep_time)
        self.right_motor.throttle = self.set_min_max(-speed)

    def stop(self):
        self.left_motor.throttle = 0.0
        sleep(sleep_time)
        self.right_motor.throttle = 0.0
