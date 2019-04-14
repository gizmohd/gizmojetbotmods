
import opc, time
# import traitlets
# from traitlets.config.configurable import Configurable


class Lights:

    headlight_left  = [64, 65, 74, 75]
    headlight_right = [72, 73, 82, 83]

    def __init__(self, num_leds=128):
        self._lights = [(0, 0, 0)] * num_leds
        self._client = opc.Client('localhost:7890')

    def set_left_headlight(self, color):
        for l in self.headlight_left:
            self._lights[l] = color
            self._client.put_pixels(self._lights)

    def set_right_headlight(self, color):
        for l in self.headlight_right:
            self._lights[l] = color
            self._client.put_pixels(self._lights)

    def set_headlights(self, color):
        self.set_left_headlight(color)
        self.set_right_headlight(color)

#TODO:  Night Rider Effect!