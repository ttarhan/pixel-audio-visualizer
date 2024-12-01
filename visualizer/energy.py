import numpy as np
from scipy import fftpack as fft

from .effect import Effect

# Using max on amplitude
# ENERGY_LOW = 0.1
# ENERGY_HIGH = 0.5

# Using max on fft
# ENERGY_LOW = 10
# ENERGY_HIGH = 70

# Using ssq on fft
# ENERGY_LOW = 900
# ENERGY_HIGH = 10000

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]

class AudioEnergy(Effect):
    """
    A simple meter that lights up pixels to a "height" based on the volume between below a low pass filter
    """

    def __init__(self, sampleinfo, led_count, energylow, energyhigh, energylowpass, color_index, flashratio):
        super().__init__(led_count)
        self.sampleinfo = sampleinfo
        self.energylow = energylow
        self.energyhigh = energyhigh
        self.energylowpass = energylowpass
        self.color_index = color_index
        self.flashratio = flashratio

        self.energyrange = self.energyhigh - self.energylow

        self.frequencies = fft.rfftfreq(sampleinfo.chunk, 1/sampleinfo.rate)
        self.lowpass_cutoff = self.frequencies[self.frequencies < self.energylow]
        self.color_frames = 0

    def render(self, audio, audiofft, data):
        filteredudio = audiofft[self.frequencies < self.energylowpass]
        ssq = np.sum(filteredudio**2)

        if ssq < self.energylow:
            return

        height = (ssq - self.energylow) / self.energyrange * self.led_count
        height = int(min(height, self.led_count))

        if height > self.led_count * self.flashratio:
            self.color_frames = 0
            self.color_index += 1

        self.color_frames += 1

        data[0:0 + height] = COLORS[self.color_index % len(COLORS)]