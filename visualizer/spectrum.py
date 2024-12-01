import numpy as np
from scipy import fftpack as fft

from .effect import Effect

COLORS = [
    (0, 0, 255),
    (0, 255, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 128, 0),
    (255, 0, 0),
    (255, 0, 255) 
]

class AudioSpectrum(Effect):
    """
    AudioSpectrum
    """

    def __init__(self, sampleinfo, led_count, *, lowfreq=50, highfreq=4500, energylow=10, energyhigh=50, reverse=False):
        super().__init__(led_count)
        self.sampleinfo = sampleinfo

        self.frequencies = fft.rfftfreq(sampleinfo.chunk, 1/sampleinfo.rate)
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

        self.ln = None

    def render(self, audio, audiofft, data):
        # dBS = 10 * np.log10(audiofft)

        newvalues = list(groupbins(self.binned, audiofft))
        maxvalues = [max(m) if len(m) else 0 for m in newvalues]
        # maxvalues = [sum(map(lambda x:x*x,m)) if len(m) else 0 for m in newvalues]

        buffer = np.full((self.led_count, 3), 0, dtype = np.uint8)

        for (i,v) in enumerate(maxvalues):
            if v < self.energylow:
                continue

            colorindex = (v - self.energylow) / self.energyrange * (len(COLORS) - 1)
            colorindex = int(min(colorindex, len(COLORS) - 1))
            
            chan = self.led_offset + i * self.led_multiple
            endchan = chan + self.led_multiple - 1
            buffer[chan:endchan + 1] = COLORS[colorindex]

        data[0:0 + self.led_count] = np.flip(buffer, 0) if self.reverse else buffer

        if self.ln is not None:
            self.ln.remove()

        # self.ln, = plt.plot(self.frequencies,audiofft)
        # self.ln, = plt.plot(np.reshape(dmx,-1))
        # plt.pause(0.005)
        # print(f'Diff: {round(time.time()-lt,4)}')

def groupbins(bins, data):
    current = []
    curbin = bins[0]

    for (i,d) in enumerate(bins):
        if d != curbin:
            yield current
            current = []
            curbin = d

        current.append(data[i])
    
    yield current