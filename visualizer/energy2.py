import numpy as np
from scipy import fftpack as fft

from .effect import Effect, Context, ChannelData
from .audiodatasource import AudioDataSource, SampleInfo

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
    (255, 0, 255),
]


class AudioEnergy2(Effect):
    """
    A simple meter based on the volume between below a low pass filter
    """

    def __init__(
        self,
        sampleinfo: SampleInfo,
        led_count: int,
        *,
        energylow: int = 900,
        energyhigh: int = 30000,
        energylowpass: int = 120,
        color_index: int = 0,
        flashratio: float = 0.9,
    ):
        super().__init__(led_count)
        self.sampleinfo = sampleinfo
        self.energylow = energylow
        self.energyhigh = energyhigh
        self.energylowpass = energylowpass
        self.color_index = color_index
        self.flashratio = flashratio

        self.energyrange = self.energyhigh - self.energylow

        self.frequencies = fft.rfftfreq(sampleinfo.chunk, 1 / sampleinfo.rate)
        self.lowpass_cutoff = self.frequencies[self.frequencies < self.energylow]
        self.color_frames = 0

    def render(self, context: Context, channel_data: ChannelData) -> None:
        audiods = AudioDataSource.from_context(context)

        if audiods is None or audiods.audio_data_fft is None:
            return

        filteredudio = audiods.audio_data_fft[self.frequencies < self.energylowpass]
        # maxenergy = np.max(filteredudio)

        ssq = np.sum(filteredudio**2)

        # if ssq < self.energylow:
        #    return

        brightness = (ssq - self.energylow) / self.energyrange * 0.75 + 0.25
        brightness = min(brightness, 1)

        if brightness > self.flashratio:
            self.color_frames = 0
            self.color_index += 1

        self.color_frames += 1

        channel_data[0 : 0 + self.led_count] = np.asarray(COLORS[self.color_index % len(COLORS)]) * np.asarray(
            (brightness, brightness, brightness)
        )
