import threading

import numpy as np
import zmq

from .datasource import DataSource


class CvDataSource(DataSource):
    """
    A data source that provides human tracking via CV (using pixel-human-tracker)
    """

    POSITION = "position"

    def __init__(self, inactive_nohuman_frames: float, adjustment: float = 0) -> None:
        self.inactive_nohuman_frames = inactive_nohuman_frames
        self.nohuman_frames = 0
        self.adjustment = adjustment
        self.position = 0
        self.active = False

    def start(self) -> None:
        threading.Thread(target=self._start_thread).start()

    def process(self) -> None:
        pass

    def _start_thread(self) -> None:
        ctx = zmq.Context.instance()
        subscriber = ctx.socket(zmq.SUB)
        subscriber.set_hwm(1)
        subscriber.connect("tcp://pixel-human-tracker.pixels:5576")
        subscriber.setsockopt_string(zmq.SUBSCRIBE, optval="")

        while True:
            msg = subscriber.recv_pyobj()

            if len(msg) == 0 or np.all(msg == 0):
                self.position = 0
                self.nohuman_frames += 1

                if self.active and self.nohuman_frames > self.inactive_nohuman_frames:
                    print("CV inactive")
                    self.active = False

                continue

            self.nohuman_frames = 0

            if not self.active:
                print("CV active")
                self.active = True

            self.position = 1.0 - (np.max(msg[msg != 0]) + self.adjustment)

    def is_active(self) -> bool:
        """
        Returns true if cv is currently being produced
        """
        return self.active
