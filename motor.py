import atexit
from adafruit_motorkit import MotorKit
import traitlets
from traitlets.config.configurable import Configurable


class Motor(Configurable):

    value = traitlets.Float()
    
    # config
    alpha = traitlets.Float(default_value=1.0).tag(config=True)
    beta = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, driver, channel, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)  # initializes traitlets

        self._driver = driver
        if (channel == 1):
            self._motor = self._driver.motor1
        else:
            self._motor = self._driver.motor2
        atexit.register(self._release)

    def set_min_max(self, speed):
        if (speed == 0):
           return speed
        elif (speed > 1):
           return 1
        elif (speed < -1):
           return -1
        else:
           return speed
        #elif (speed > 0):
        #   return  0.3 + (speed * .7)
        #else:
        #   return  -0.3 - (speed * .7)


    @traitlets.observe('value')
    def _observe_value(self, change):
        self._write_value(change['new'])

    def _write_value(self, value):
        newval = 0
        """Sets motor value between [-1, 1]"""
#        self._motor.throttle =self.set_min_max(value)
        if (value > 0.01):
            newval = value + 0.3
        if (value < 0.01 and value > -0.01):
            value = 0
        elif (value < -0.01):
            newval = value - 0.3
        else:
            newval = value

        if (newval > 1):
            newval = 1
        elif (newval < -1):
            newval = -1

        self._motor.throttle = newval

    def _release(self):
        self._motor.throttle = 0
