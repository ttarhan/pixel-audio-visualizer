import threading

import numpy as np
import zmq

from .datasource import DataSource


class CvDataSource(DataSource):
    """
    A data source that provides human tracking via CV (using pixel-human-tracker)
    """

    def __init__(self) -> None:
        self.position = 0
        self.active = True

    def start(self) -> None:
        threading.Thread(target=self._start_thread).start()

    def process(self) -> None:
        pass

    def _start_thread(self) -> None:
        ctx = zmq.Context.instance()
        subscriber = ctx.socket(zmq.SUB)
        subscriber.connect("tcp://10.1.111.146:5576")
        subscriber.setsockopt_string(zmq.SUBSCRIBE, optval="")

        while True:
            msg = subscriber.recv_pyobj()

            if len(msg) == 0 or np.all(msg == 0):
                self.position = 0
                continue

            self.position = 1.0 - np.min(msg[msg != 0])

    def is_active(self) -> bool:
        """
        Returns true if cv is currently being produced
        """
        return self.active
