import math
from dataclasses import dataclass

import numpy as np

from .effect import Effect

MAX_PIXELS_PER_UNIVERSE = 170

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

    def __init__(self, start_universe, led_count):
        self.start_universe = start_universe
        self.led_count = led_count
        self.num_universes = math.ceil(led_count/MAX_PIXELS_PER_UNIVERSE)
        self.effects = []

    def add_effect(self, effect, position = 0):
        """
        Add an effect to the element at the given position
        """
        self.effects.append(EffectInstance(
            position  = position,
            led_count = effect.led_count if effect.led_count else self.led_count,
            effect    = effect
        ))

    def get_universes(self):
        """
        Return a tuple of universes used by this effect
        """
        return tuple(range(self.start_universe, self.start_universe + self.num_universes))

    def render(self, audio, audiofft):
        """
        Render the Element with the given audio
        """
        channel_data = np.full((self.led_count, 3), 0, dtype = np.uint8)

        for e in self.effects:
            e.effect.render(audio, audiofft, channel_data[e.position : e.position + e.led_count])

        return self._as_universe_data(channel_data)

    def _as_universe_data(self, channel_data):
        universe_data = dict()

        chan = 0

        for i in range(self.num_universes):
            universe = self.start_universe + i
            remaining_leds = self.led_count - chan
            count = min(MAX_PIXELS_PER_UNIVERSE, remaining_leds)
            endchan = chan + count - 1

            # print(f'U: {universe}, Chan: {chan}, End: {endchan}, Count: {count}')

            universe_data[universe] = np.zeros((MAX_PIXELS_PER_UNIVERSE, 3), dtype = np.uint8)
            universe_data[universe][:count] = channel_data[chan:endchan + 1]

            chan += count

        return universe_data