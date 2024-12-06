import math
from typing import Type

from .datasource import DataSource
from .effect import Effect, Context, ChannelData


class ChaserEffect(Effect):
    """
    An effect that chases a position (as defined by a data source)
    """

    def __init__(self, led_count: int, datasource_cls: Type[DataSource], datasource_attribute: str):
        super().__init__(led_count)
        self.datasource_cls = datasource_cls
        self.datasource_attribute = datasource_attribute

    def render(self, context: Context, channel_data: ChannelData) -> None:
        position = getattr(self.datasource_cls.from_context(context), self.datasource_attribute)
        maxpos = int(math.ceil(self.led_count * position))

        if maxpos > 0:
            channel_data[0:maxpos] = [255, 255, 255]
