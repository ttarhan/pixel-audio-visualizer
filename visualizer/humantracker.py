import math
import threading

import numpy as np
import zmq

from .effect import Effect

class HumanTrackerEffect(Effect):
    """
    Moves lights in response to people
    """

    def __init__(self, led_count):
        super().__init__(led_count)
        self.position = 0

        threading.Thread(target=self.start).start()

    def render(self, context, channel_data):
        maxpos = int(math.ceil(self.led_count * self.position))

        if maxpos > 0:
            channel_data[0:maxpos] = [255,255,255]

    def start(self):
        ctx = zmq.Context.instance()
        subscriber = ctx.socket(zmq.SUB)
        subscriber.connect(f"tcp://10.1.111.146:5576")
        subscriber.setsockopt_string(zmq.SUBSCRIBE, optval="")

        while True:
            msg = subscriber.recv_pyobj()

            if len(msg) == 0 or np.all(msg == 0):
                self.position = 0
                continue

            self.position = 1.0 - np.min(msg[msg != 0])