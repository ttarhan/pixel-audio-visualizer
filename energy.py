import numpy as np
from scipy import fftpack as fft

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

class AudioEnergy(object):

    def __init__(self, sampleinfo, startchannel, ledcount, energylow, energyhigh, energylowpass, color_index, flashratio):
        self.sampleinfo = sampleinfo
        self.startchannel = startchannel
        self.ledcount = ledcount
        self.energylow = energylow
        self.energyhigh = energyhigh
        self.energylowpass = energylowpass
        self.color_index = color_index
        self.flashratio = flashratio

        self.energyrange = self.energyhigh - self.energylow

        self.frequencies = fft.rfftfreq(sampleinfo.chunk, 1/sampleinfo.rate)
        self.lowpass_cutoff = self.frequencies[self.frequencies < self.energylow]
        self.color_frames = 0

    def frame(self, audio, audiofft, dmx):
        filteredudio = audiofft[self.frequencies < self.energylowpass]
        # maxenergy = np.max(filteredudio)
        ssq = np.sum(filteredudio**2)

        if ssq < self.energylow:
            return

        height = (ssq - self.energylow) / self.energyrange * self.ledcount
        height = int(min(height, self.ledcount))

        # if self.color_frames > self.sampleinfo.fps * 0.5 and height > 75:
        if height > self.ledcount * self.flashratio:
            self.color_frames = 0
            self.color_index += 1

        self.color_frames += 1

        dmx[self.startchannel:self.startchannel + height] = COLORS[self.color_index % len(COLORS)]