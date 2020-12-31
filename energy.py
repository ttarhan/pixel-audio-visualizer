import numpy as np
from scipy import fftpack as fft

# Using max on amplitude
# ENERGY_LOW = 0.1
# ENERGY_HIGH = 0.5

# Using max on fft
# ENERGY_LOW = 10
# ENERGY_HIGH = 70

# Using ssq on fft
ENERGY_LOW = 900
ENERGY_HIGH = 10000

ENERGY_RANGE = ENERGY_HIGH - ENERGY_LOW

ENERGY_FILTER_LOWPASS = 120

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]

class AudioEnergy(object):

    def __init__(self, sampleinfo, startchannel, ledcount, color_index = 0):
        self.sampleinfo = sampleinfo
        self.startchannel = startchannel
        self.ledcount = ledcount
        self.color_index = color_index

        self.frequencies = fft.rfftfreq(sampleinfo.chunk, 1/sampleinfo.rate)
        self.lowpass_cutoff = self.frequencies[self.frequencies < ENERGY_LOW]
        self.color_frames = 0

    def frame(self, audio, audiofft, dmx):
        filteredudio = audiofft[self.frequencies < ENERGY_FILTER_LOWPASS]
        # maxenergy = np.max(filteredudio)
        ssq = np.sum(filteredudio**2)

        if ssq < ENERGY_LOW:
            return

        height = (ssq - ENERGY_LOW) / ENERGY_RANGE * self.ledcount
        height = int(min(height, self.ledcount))

        # if self.color_frames > self.sampleinfo.fps * 0.5 and height > 75:
        if height > 75:
            self.color_frames = 0
            self.color_index += 1

        self.color_frames += 1

        dmx[self.startchannel:self.startchannel + height] = COLORS[self.color_index % len(COLORS)]