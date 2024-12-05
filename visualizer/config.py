from dataclasses import dataclass
import pyaudio

from .element import Element
from .audiodatasource import AudioDataSource
from .cvdatasource import CvDataSource

from .spectrum import AudioSpectrum
from .energy import AudioEnergy
from .energy2 import AudioEnergy2
from .chaser import ChaserEffect
from .testeffect import TestEffect

@dataclass
class SampleInfo(object):
    rate: int
    chunk: int
    fps: int
    format: int
    channels: int

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
    fps = FRAME_FPS,
    format = FORMAT,
    channels = CHANNELS
)

audiods = AudioDataSource(SAMPLE_INFO, SILENCE_THRESHOLD, SILENCE_SECONDS)
cvds = CvDataSource()

CLOCK_SOURCE = audiods
DATA_SOURCES = {
    AudioDataSource.context_key(): audiods,
    CvDataSource.context_key(): cvds
}

pool_side = Element(audiods.is_active, 5, 412)
pool_side.add_effect(AudioSpectrum(SAMPLE_INFO, 206), position=0)
pool_side.add_effect(AudioSpectrum(SAMPLE_INFO, 206, reverse=True), position=206)

pool_tree_one = Element(audiods.is_active, 8, 100)
pool_tree_one.add_effect(AudioEnergy(SAMPLE_INFO, pool_tree_one.led_count))

pool_tree_two = Element(audiods.is_active, 9, 100)
pool_tree_two.add_effect(AudioEnergy(SAMPLE_INFO, pool_tree_two.led_count, color_index=1))

kylies_room = Element(audiods.is_active, 12, 221)
kylies_room.add_effect(AudioSpectrum(SAMPLE_INFO, kylies_room.led_count))

# test_element = Element(15, 100)

step1 = Element(cvds.is_active, 110, 232) # Wrong number of pixels
step2 = Element(cvds.is_active, 120, 196)
step3 = Element(cvds.is_active, 130, 232)

step1.add_effect(ChaserEffect(step1.led_count, CvDataSource, "position"))
step2.add_effect(ChaserEffect(step2.led_count, CvDataSource, "position"))
step3.add_effect(ChaserEffect(step3.led_count, CvDataSource, "position"))

ELEMENTS = [pool_side, pool_tree_one, pool_tree_two, step3]
