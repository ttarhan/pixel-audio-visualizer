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

pool_side = Element(5, 412)
pool_side.add_effect(AudioSpectrum(SAMPLE_INFO, 206), position=0)
pool_side.add_effect(AudioSpectrum(SAMPLE_INFO, 206, reverse=True), position=206)

pool_tree_one = Element(8, 100)
pool_tree_one.add_effect(AudioEnergy(SAMPLE_INFO, pool_tree_one.led_count))

pool_tree_two = Element(9, 100)
pool_tree_two.add_effect(AudioEnergy(SAMPLE_INFO, pool_tree_two.led_count, color_index=1))

kylies_room = Element(12, 221)
kylies_room.add_effect(AudioSpectrum(SAMPLE_INFO, kylies_room.led_count))

test_element = Element(15, 100)

AUDIO_ELEMENTS = [pool_side, pool_tree_one, pool_tree_two, kylies_room]
FULLTIME_ELEMENTS = [test_element]

ELEMENTS = [*AUDIO_ELEMENTS, *FULLTIME_ELEMENTS]
