import pyaudio

from .element import Element
from .audiodatasource import AudioDataSource, SampleInfo
from .cvdatasource import CvDataSource

from .spectrum import AudioSpectrum
from .energy import AudioEnergy
from .chaser import ChaserEffect


FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 48000
DMX_FPS = 50
FRAME_FPS = 25

SILENCE_THRESHOLD = 0.05
SILENCE_SECONDS = 5
CHUNK = int(RATE / FRAME_FPS)

SAMPLE_INFO = SampleInfo(rate=RATE, chunk=CHUNK, fps=FRAME_FPS, format=FORMAT, channels=CHANNELS)

CV_INACTIVE_SECONDS = 2

audiods = AudioDataSource(SAMPLE_INFO, SILENCE_THRESHOLD, SILENCE_SECONDS)
cvds = CvDataSource(CV_INACTIVE_SECONDS * SAMPLE_INFO.fps, adjustment = 0.02)

CLOCK_SOURCE = audiods
DATA_SOURCES = {
    AudioDataSource.context_key(): audiods,
    CvDataSource.context_key(): cvds,
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

step1 = Element(cvds.is_active, 110, 90)
step2 = Element(cvds.is_active, 120, 196)
step3 = Element(cvds.is_active, 130, 232)

step1.add_effect(ChaserEffect(step1.led_count, CvDataSource, CvDataSource.POSITION, start=0.644, end=1.000))
step2.add_effect(ChaserEffect(step2.led_count, CvDataSource, CvDataSource.POSITION, start=0.220, end=1.000))
step3.add_effect(ChaserEffect(step3.led_count, CvDataSource, CvDataSource.POSITION, start=0.000, end=0.924))


ELEMENTS = [pool_side, pool_tree_one, pool_tree_two, kylies_room, step1, step2, step3]
