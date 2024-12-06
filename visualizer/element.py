import math
from dataclasses import dataclass
from typing import Tuple, Dict, Callable, Union, List

import numpy as np
from numpy.typing import NDArray

from .effect import Effect, Context, ChannelData

MAX_PIXELS_PER_UNIVERSE = 170

UniverseData = Dict[int, NDArray[np.uint8]]


@dataclass
class EffectInstance:
    """
    An effect that's been added to an Element
    """

    position: int
    led_count: int
    effect: Effect


class Element:
    """
    Represents a physical element like a string of LED pixels or an LED strip.
    """

    def __init__(self, active_criteria: Union[Callable[[], bool], bool], start_universe: int, led_count: int):
        self.active_criteria = active_criteria
        self.start_universe = start_universe
        self.led_count = led_count
        self.num_universes = math.ceil(led_count / MAX_PIXELS_PER_UNIVERSE)
        self.effects: List[EffectInstance] = []

    def add_effect(self, effect: Effect, position: int = 0) -> None:
        """
        Add an effect to the element at the given position
        """
        self.effects.append(
            EffectInstance(
                position=position,
                led_count=effect.led_count if effect.led_count else self.led_count,
                effect=effect,
            )
        )

    def get_universes(self) -> Tuple[int, ...]:
        """
        Return a tuple of universes used by this effect
        """
        return tuple(range(self.start_universe, self.start_universe + self.num_universes))

    def render(self, context: Context) -> UniverseData:
        """
        Render the Element (with the given audio, if available)
        """
        channel_data = np.full((self.led_count, 3), 0, dtype=np.uint8)

        for e in self.effects:
            e.effect.render(context, channel_data[e.position : e.position + e.led_count])

        return self._as_universe_data(channel_data)

    def is_active(self) -> bool:
        """
        Return true if the Element is active
        """

        return self.active_criteria() if callable(self.active_criteria) else self.active_criteria

    def _as_universe_data(self, channel_data: ChannelData) -> UniverseData:
        universe_data = {}

        chan = 0

        for i in range(self.num_universes):
            universe = self.start_universe + i
            remaining_leds = self.led_count - chan
            count = min(MAX_PIXELS_PER_UNIVERSE, remaining_leds)
            endchan = chan + count - 1

            # print(f'U: {universe}, Chan: {chan}, End: {endchan}, Count: {count}')

            universe_data[universe] = np.zeros((MAX_PIXELS_PER_UNIVERSE, 3), dtype=np.uint8)
            universe_data[universe][:count] = channel_data[chan : endchan + 1]

            chan += count

        return universe_data
