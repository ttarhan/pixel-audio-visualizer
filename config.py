from dataclasses import dataclass
import pyaudio
from spectrum import AudioSpectrum
from energy import AudioEnergy

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

PROCESSORS = [
    AudioSpectrum(SAMPLE_INFO, 0, 206, 50, 4500, 10, 50, False),
    AudioSpectrum(SAMPLE_INFO, 206, 206, 50, 4500, 10, 50, True),
    AudioEnergy(SAMPLE_INFO, 412, 100, 900, 10000, 120, 0, 0.75),
    AudioEnergy(SAMPLE_INFO, 512, 100, 900, 10000, 120, 1, 0.75),
    AudioSpectrum(SAMPLE_INFO, 612, 50, 50, 1300, 20, 50, False),
    # AudioSpectrum(SAMPLE_INFO, 662, 50, 50, 1300, 20, 50)
    AudioEnergy(SAMPLE_INFO, 662, 50, 900, 10000, 120, 0, .99)
]

UNIVERSE_START = 5
UNIVERSE_LAYOUT = [170, 170, 72, 100, 100, 50, 50]
LEDS = sum(UNIVERSE_LAYOUT)