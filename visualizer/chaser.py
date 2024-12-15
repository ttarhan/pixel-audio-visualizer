from typing import Type

import numpy as np

from .datasource import DataSource
from .effect import Effect, Context, ChannelData

SPREAD_LEFT_COLOR = [255, 0, 0]
SPREAD_RIGHT_COLOR = [0, 255, 0]
MIDPOINT_COLOR = [255, 255, 255]


class ChaserEffect(Effect):
    """
    An effect that chases a position (as defined by a data source)
    """

    def __init__(
        self,
        led_count: int,
        datasource_cls: Type[DataSource],
        datasource_attribute: str,
        *,
        start: float = 0.0,
        end: float = 1.0,
        spread: int = 5,
    ):
        super().__init__(led_count)
        self.datasource_cls = datasource_cls
        self.datasource_attribute = datasource_attribute
        self.start = start
        self.end = end
        self.spread = spread
        self.multipliers = np.linspace(0, 1, spread)
        self.multipliers = self.multipliers[:, np.newaxis] * np.ones(3)  # Broadcasting to RGB

    def render(self, context: Context, channel_data: ChannelData) -> None:
        position = getattr(self.datasource_cls.from_context(context), self.datasource_attribute)

        if position < self.start or position > self.end:
            return

        led_spacing = (self.end - self.start) / (self.led_count - 1)

        # Find the closest LED to the position
        relative_pos = position - self.start
        led_index = round(relative_pos / led_spacing)

        # Ensure we don't exceed strip bounds
        led_index = max(0, min(led_index, self.led_count - 1))

        channel_data[led_index] = MIDPOINT_COLOR

        left_spread = min(led_index, self.spread)
        right_spread = min(self.led_count - led_index - 1, self.spread)

        print(
            f"I: {led_index}, L: {left_spread}, R: {right_spread}     CDL: {led_index - left_spread} : {led_index}    CDR: {led_index + 1} : {led_index + 1 + right_spread}"
        )

        channel_data[led_index - left_spread : led_index] = np.round(SPREAD_LEFT_COLOR * self.multipliers)[
            0:left_spread
        ]
        channel_data[led_index + 1 : led_index + 1 + right_spread] = np.round(
            SPREAD_RIGHT_COLOR * self.multipliers[::-1]
        )[0:right_spread]

        # print(led_index)
