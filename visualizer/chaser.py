import math
import threading

import numpy as np
import zmq

from .effect import Effect

class ChaserEffect(Effect):
    """
    An effect that chases a position (as defined by a data source)
    """

    def __init__(self, led_count, datasource_cls, datasource_attribute):
        super().__init__(led_count)
        self.datasource_cls = datasource_cls
        self.datasource_attribute = datasource_attribute

    def render(self, context, channel_data):
        position = getattr(self.datasource_cls.from_context(context), self.datasource_attribute)
        maxpos = int(math.ceil(self.led_count * position))

        if maxpos > 0:
            channel_data[0:maxpos] = [255,255,255]
