from abc import ABC, abstractmethod


class Effect(ABC):
    """
    Represents an effect that will be added to an element
    """

    def __init__(self, led_count):
        self.led_count = led_count

    @abstractmethod
    def render(self, context, channel_data):
        """
        Render the effect with the given audio
        """
