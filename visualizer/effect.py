from abc import ABC, abstractmethod
from typing import Dict, Any

import numpy as np
from numpy.typing import NDArray

Context = Dict[str, Any]
ChannelData = NDArray[np.uint8]


class Effect(ABC):
    """
    Represents an effect that will be added to an element
    """

    def __init__(self, led_count: int):
        self.led_count = led_count

    @abstractmethod
    def render(self, context: Context, channel_data: ChannelData) -> None:
        """
        Render the effect with the given audio
        """
