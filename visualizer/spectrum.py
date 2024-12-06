from typing import List, Iterator

import numpy as np
from numpy.typing import NDArray
from scipy import fftpack as fft


from .effect import Effect, Context, ChannelData
from .audiodatasource import AudioDataSource, SampleInfo

COLORS = [
    (0, 0, 255),
    (0, 255, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 128, 0),
    (255, 0, 0),
    (255, 0, 255),
]


class AudioSpectrum(Effect):
    """
    AudioSpectrum
    """

    def __init__(
        self,
        sampleinfo: SampleInfo,
        led_count: int,
        *,
        lowfreq: int = 50,
        highfreq: int = 4500,
        energylow: int = 10,
        energyhigh: int = 50,
        reverse: bool = False,
    ):
        super().__init__(led_count)
        self.sampleinfo = sampleinfo

        self.frequencies = fft.rfftfreq(sampleinfo.chunk, 1 / sampleinfo.rate)
        self.energylow = energylow
        self.energyhigh = energyhigh
        self.energyrange = self.energyhigh - self.energylow
        self.reverse = reverse

        bins = np.linspace(lowfreq, highfreq, self.led_count)
        binned = np.digitize(self.frequencies, bins)

        # Digitize returns a bin after our last bin for out-of-range items; chop it off
        self.binned = binned[binned < self.led_count]

        # How many unique bins did we end up with?
        usable_bins = np.unique(self.binned).size

        self.led_multiple = int(self.led_count / usable_bins)
        self.led_offset = int((self.led_count - usable_bins * self.led_multiple) / 2)

        # self.ln = None

    def render(self, context: Context, channel_data: ChannelData) -> None:
        audiods = AudioDataSource.from_context(context)

        if audiods is None or audiods.audio_data_fft is None:
            return

        audiofft = audiods.audio_data_fft

        # dBS = 10 * np.log10(audiofft)

        newvalues = list(_groupbins(self.binned, audiofft))
        maxvalues = [max(m) if len(m) else 0 for m in newvalues]
        # maxvalues = [sum(map(lambda x:x*x,m)) if len(m) else 0 for m in newvalues]

        buffer = np.full((self.led_count, 3), 0, dtype=np.uint8)

        for i, v in enumerate(maxvalues):
            if v < self.energylow:
                continue

            colorindex = (v - self.energylow) / self.energyrange * (len(COLORS) - 1)
            colorindex = int(min(colorindex, len(COLORS) - 1))

            chan = self.led_offset + i * self.led_multiple
            endchan = chan + self.led_multiple - 1
            buffer[chan : endchan + 1] = COLORS[colorindex]

        channel_data[0 : 0 + self.led_count] = np.flip(buffer, 0) if self.reverse else buffer

        # if self.ln is not None:
        #     self.ln.remove()
        # self.ln, = plt.plot(self.frequencies,audiofft)
        # self.ln, = plt.plot(np.reshape(dmx,-1))
        # plt.pause(0.005)
        # print(f'Diff: {round(time.time()-lt,4)}')


def _groupbins(bins: NDArray[np.intp], data: NDArray[np.float32]) -> Iterator[List[float]]:
    current: List[float] = []
    curbin = bins[0]

    for i, d in enumerate(bins):
        if d != curbin:
            yield current
            current = []
            curbin = d

        current.append(data[i])

    yield current
