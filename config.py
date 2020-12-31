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
    AudioSpectrum(SAMPLE_INFO, 0, 412),
    AudioEnergy(SAMPLE_INFO, 412, 100, 0),
    AudioEnergy(SAMPLE_INFO, 512, 100, 1)
]

UNIVERSE_START = 5
UNIVERSE_LAYOUT = [170, 170, 72, 100, 100]
LEDS = sum(UNIVERSE_LAYOUT)