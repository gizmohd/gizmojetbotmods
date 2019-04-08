from time import sleep
import traitlets
from traitlets.config.configurable import SingletonConfigurable
from adafruit_motorkit import MotorKit
from .motor import Motor
from .PCA9685 import PCA9685

sleep_time = 0.05

class Robot(SingletonConfigurable):
    
    left_motor = traitlets.Instance(Motor) 
    right_motor = traitlets.Instance(Motor)
    # config
    left_motor_channel = traitlets.Integer(default_value=2).tag(config=True)
    left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    right_motor_channel = traitlets.Integer(default_value=1).tag(config=True)
    right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)

    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        self.motor_driver = MotorKit(0x40)
        self.servo_driver = PCA9685(0x70)
        self.setPWMFreq(50)
        self.left_motor = Motor(self.motor_driver, channel=self.left_motor_channel, alpha=self.left_motor_alpha)
        self.right_motor = Motor(self.motor_driver, channel=self.right_motor_channel, alpha=self.right_motor_alpha)

    def set_servo(self, id, position):
        self.servo_driver.setServoPulse(id, position)

    def set_motors(self, left_speed, right_speed):
        self.left_motor.value = left_speed
        self.right_motor.value = right_speed

    def forward(self, speed=1.0, duration=None):
        self.left_motor.value = speed
        self.right_motor.value = speed

    def backward(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = -speed

    def left(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = speed

    def right(self, speed=1.0):
        self.left_motor.value = speed
        self.right_motor.value = -speed

    def stop(self):
        self.left_motor.value = 0
        self.right_motor.value = 0
