from dataclasses import dataclass
import pyaudio

from .element import Element

from .spectrum import AudioSpectrum
from .energy import AudioEnergy
from .energy2 import AudioEnergy2
from .testeffect import TestEffect

@dataclass
class SampleInfo(object):
    rate: int
    chunk: int
    fps: int

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000
DMX_FPS = 50
FRAME_FPS = 25

SILENCE_THRESHOLD = 0.05
SILENCE_SECONDS = 5
CHUNK = int(RATE/FRAME_FPS)

SAMPLE_INFO = SampleInfo(
    rate = RATE,
    chunk = CHUNK,
    fps = FRAME_FPS
)

# PROCESSORS = [
#     AudioSpectrum(SAMPLE_INFO, 0, 206, 50, 4500, 10, 50, False),
#     AudioSpectrum(SAMPLE_INFO, 206, 206, 50, 4500, 10, 50, True),
#     AudioEnergy(SAMPLE_INFO, 412, 100, 900, 10000, 120, 0, 0.75),
#     AudioEnergy(SAMPLE_INFO, 512, 100, 900, 10000, 120, 1, 0.75),
#     # AudioSpectrum(SAMPLE_INFO, 612, 50, 50, 1300, 20, 50, False),
#     # AudioSpectrum(SAMPLE_INFO, 662, 50, 50, 1300, 20, 50)
#     # AudioEnergy(SAMPLE_INFO, 662, 50, 900, 10000, 120, 0, .99)
#     AudioEnergy(SAMPLE_INFO, 612, 100, 900, 10000, 120, 2, 0.75),
#     AudioEnergy2(SAMPLE_INFO, 712, 85, 900, 30000, 120, 0, 0.90),
#     AudioSpectrum(SAMPLE_INFO, 797, 221, 50, 4500, 10, 50, False),
#     # AudioSpectrum(SAMPLE_INFO, 1056, 209, 50, 4500, 10, 50, True),
#     # AudioEnergy(SAMPLE_INFO, 1056, 209, 800, 10000, 90, 0, 0.99)
# ]
#     #def __init__(self, sampleinfo, startchannel, ledcount, lowfreq, highfreq, energylow, energyhigh, reverse):
#     #def __init__(self, sampleinfo, startchannel, ledcount, energylow, energyhigh, energylowpass, color_index, flashratio):

# kylies_room = Element(12, 221)
# kylies_room.add_effect(AudioEnergy(SAMPLE_INFO, kylies_room.led_count, 900, 10000, 120, 2, 0.75))

# ELEMENTS = [kylies_room]

testel = Element(5, 341)
testel.add_effect(TestEffect(341))

ELEMENTS = [testel]


# UNIVERSE_START = 5
# #UNIVERSE_LAYOUT = [170, 170, 72, 100, 100, 50, 50]
# UNIVERSE_LAYOUT = [170, 170, 72, 100, 100, 100, 85, 170, 51]
# LEDS = sum(UNIVERSE_LAYOUT)
