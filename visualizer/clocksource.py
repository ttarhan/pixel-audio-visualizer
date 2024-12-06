from abc import ABC, abstractmethod


class ClockSource(ABC):
    """
    A timing source used to control element/effect rendering
    """

    @abstractmethod
    def start(self) -> None:
        """
        Start the clock
        """

    @abstractmethod
    def tick(self) -> None:
        """
        Block until the next clock cycle, then return
        """
