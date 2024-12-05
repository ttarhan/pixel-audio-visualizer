from abc import ABC, abstractmethod


class ClockSource(ABC):
    """
    A timing source used to control element/effect rendering
    """

    @abstractmethod
    def start(self):
        """
        Start the clock
        """

    @abstractmethod
    def tick(self):
        """
        Block until the next clock cycle, then return
        """
