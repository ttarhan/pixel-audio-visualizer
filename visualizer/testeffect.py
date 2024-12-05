import numpy as np

from .effect import Effect

class TestEffect(Effect):
    """
    A simple test effect
    """

    def __init__(self, led_count):
        super().__init__(led_count)

    def render(self, context, channel_data):
        channel_data[0:self.led_count] = np.reshape(range(0,self.led_count * 3), (-1, 3))