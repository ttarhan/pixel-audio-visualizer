import numpy as np
from matplotlib import pyplot as plt
from scipy import fftpack as fft

COLORS = [
    (0, 0, 255),
    (0, 255, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 128, 0),
    (255, 0, 0),
    (255, 0, 255) 
]

class AudioSpectrum(object):

    def __init__(self, sampleinfo, startchannel, ledcount, lowfreq, highfreq, energylow, energyhigh):
        self.startchannel = startchannel
        self.ledcount = ledcount
        self.frequencies = fft.rfftfreq(sampleinfo.chunk, 1/sampleinfo.rate)
        self.energylow = energylow
        self.energyhigh = energyhigh
        self.energyrange = self.energyhigh - self.energylow
        
        bins = np.linspace(lowfreq, highfreq, self.ledcount)
        binned = np.digitize(self.frequencies, bins)
        
        # Digitize returns a bin after our last bin for out-of-range items; chop it off
        self.binned = binned[binned < self.ledcount]

        # How many unique bins did we end up with?
        usable_bins = np.unique(self.binned).size

        self.led_multiple = int(self.ledcount / usable_bins)
        self.led_offset = int((self.ledcount - usable_bins * self.led_multiple) / 2)

        self.ln = None

    def frame(self, audio, audiofft, dmx):
        # dBS = 10 * np.log10(audiofft)

        newvalues = list(groupbins(self.binned, audiofft))
        maxvalues = [max(m) if len(m) else 0 for m in newvalues]
        # maxvalues = [sum(map(lambda x:x*x,m)) if len(m) else 0 for m in newvalues]

        for (i,v) in enumerate(maxvalues):
            if v < self.energylow:
                continue

            colorindex = (v - self.energylow) / self.energyrange * (len(COLORS) - 1)
            colorindex = int(min(colorindex, len(COLORS) - 1))
            
            chan = self.startchannel + self.led_offset + i * self.led_multiple
            endchan = chan + self.led_multiple - 1
            dmx[chan:endchan + 1] = COLORS[colorindex]

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