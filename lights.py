
import opc
import time
import threading


# import traitlets
# from traitlets.config.configurable import Configurable


class Lights(object):

    headlight_left = [64, 65, 74, 75]
    headlight_right = [72, 73, 82, 83]
    lb_top_start = 64
    lb_bottom_start = 74

    def __init__(self, updateinterval=0.075):
        self._num_leds = 128
        self._lights = [(0, 0, 0)] * self._num_leds
        self._client = opc.Client('localhost:7890')
        self._kitt_lights_on = False
        self._klights = []
        self._klights_min = []
        self.updateinterval = updateinterval

        for n in range(10):
            self._klights.append((n + self.lb_top_start, n + self.lb_bottom_start))

        for n in range(6):
            self._klights_min.append((n + self.lb_top_start + 2, n + self.lb_bottom_start + 2))

    def lights_off(self):
        self._lights = [(0, 0, 0)] * self._num_leds
        self._client.put_pixels(self._lights)

    def set_left_headlight(self, color):
        print("Updating Lights (hl) {}".format(self.headlight_left))
        for l in self.headlight_left:
            self._lights[l] = color
            self._client.put_pixels(self._lights)

    def set_right_headlight(self, color):
        print("Updating Lights (hr) {}".format(self.headlight_right))
        for l in self.headlight_right:
            self._lights[l] = color
            self._client.put_pixels(self._lights)

    def set_headlights(self, color):
        self.set_left_headlight(color)
        self.set_right_headlight(color)

    @staticmethod
    def _change_intensity(color, percentage):
        if percentage > 1 or percentage < 0:
            raise ValueError("Percentage Value must be between 0 and 1")

        newcolor = (int(color[0] * percentage), int(color[1] * percentage), int(color[2] * percentage))
        return newcolor

    # Define some settings
    StepCounter = 0
    StepDir = 1
    WaitTime = 0.2

    # Define some sequences

    # One LED
    StepCount1 = 10
    Seq1 = []
    Seq1 = list(range(0, StepCount1))
    Seq1[0] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Seq1[1] = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    Seq1[2] = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    Seq1[3] = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    Seq1[4] = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    Seq1[5] = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    Seq1[6] = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    Seq1[7] = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    Seq1[8] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    Seq1[9] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    StepCount1a = 6
    Seq1a = []
    Seq1a = list(range(0, StepCount1a))
    Seq1a[0] = [1, 0, 0, 0, 0, 0]
    Seq1a[1] = [0, 1, 0, 0, 0, 0]
    Seq1a[2] = [0, 0, 1, 0, 0, 0]
    Seq1a[3] = [0, 0, 0, 1, 0, 0]
    Seq1a[4] = [0, 0, 0, 0, 1, 0]
    Seq1a[5] = [0, 0, 0, 0, 0, 1]

    # Double LEDs
    StepCount2 = 11
    Seq2 = []
    Seq2 = list(range(0, StepCount2))
    Seq2[0] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Seq2[1] = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    Seq2[2] = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    Seq2[3] = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
    Seq2[4] = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
    Seq2[5] = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    Seq2[6] = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
    Seq2[7] = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
    Seq2[8] = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
    Seq2[9] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    Seq2[10] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    StepCount2a = 7
    Seq2a = []
    Seq2a = list(range(0, StepCount2))
    Seq2a[0] = [1, 0, 0, 0, 0, 0]
    Seq2a[1] = [1, 1, 0, 0, 0, 0]
    Seq2a[2] = [0, 1, 1, 0, 0, 0]
    Seq2a[3] = [0, 0, 1, 1, 0, 0]
    Seq2a[4] = [0, 0, 0, 1, 1, 0]
    Seq2a[5] = [0, 0, 0, 0, 1, 1]
    Seq2a[6] = [0, 0, 0, 0, 0, 1]



    # Two LEDs from opposite ends
    StepCount3 = 9
    Seq3 = []
    Seq3 = list(range(0, StepCount3))
    Seq3[0] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    Seq3[1] = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
    Seq3[2] = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
    Seq3[3] = [0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    Seq3[4] = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    Seq3[5] = [0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    Seq3[6] = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
    Seq3[7] = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
    Seq3[8] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    StepCount3a = 5
    Seq3a = []
    Seq3a = list(range(0, StepCount3))
    Seq3a[0] = [1, 0, 0, 0, 0, 1]
    Seq3a[1] = [0, 1, 0, 0, 1, 0]
    Seq3a[2] = [0, 0, 1, 1, 0, 0]
    Seq3a[3] = [0, 1, 0, 0, 1, 0]
    Seq3a[4] = [1, 0, 0, 0, 0, 1]

    # Choose a sequence to use
    # Seq = Seq3
    # StepCount = StepCount3

    def light_test(self, color=(255, 0, 0)):
        self.lights_directional(self.Seq3, self.StepCount3, self._klights, color)

    def lights_directional(self, sequence, stepcount, lightarry, color=(255, 0, 0)):
        while True:
            for idx in range(len(lightarry)):
                new_color = Lights._change_intensity(color,  sequence[self.StepCounter][idx])
                print(new_color)
                self._lights[lightarry[idx][0]] = new_color
                self._lights[lightarry[idx][1]] = new_color

            self._client.put_pixels(self._lights)

            self.StepCounter += self.StepDir

            # If we reach the end of the sequence reverse
            # the direction and step the other way
            if (self.StepCounter == stepcount) or (self.StepCounter < 0):
                self.StepDir = self.StepDir * -1
                self.StepCounter = self.StepCounter + self.StepDir + self.StepDir

            # Wait before moving on
            time.sleep(self.WaitTime)


