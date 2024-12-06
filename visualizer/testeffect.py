import numpy as np

from .effect import Effect, Context, ChannelData


class TestEffect(Effect):
    """
    A simple test effect
    """

    def render(self, context: Context, channel_data: ChannelData) -> None:
        channel_data[0 : self.led_count] = np.reshape(range(0, self.led_count * 3), (-1, 3))
