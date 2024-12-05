import pyaudio
import numpy as np
from scipy import fftpack as fft

from .datasource import DataSource
from .clocksource import ClockSource

class AudioDataSource(DataSource, ClockSource):
    """
    A data source that reads audio data from a local audio input, and also
    serves as a clock source based on fixed-duration reads from the audio source.

    Must be used as the clock source to return audio frames.
    """

    def __init__(self, sampleinfo, silence_threshold, silence_seconds):
        self.sampleinfo = sampleinfo
        self.silence_threshold = silence_threshold
        self.silence_seconds = silence_seconds

        print(self.sampleinfo)

        self.pyaudio = None
        self.stream = None
        self.rawaudio = None
        self.silent_frames = 0
        self.active = False
        self.audio_data = None
        self.audio_data_fft = None
        self.running = False

    def start(self):
        if self.running:
            return
        
        self.pyaudio = pyaudio.PyAudio()

        self.stream = self.pyaudio.open(format=self.sampleinfo.format,
                                      channels=self.sampleinfo.channels,
                                      rate=self.sampleinfo.rate,
                                      input=True,
                                      frames_per_buffer=self.sampleinfo.chunk)

        self.running = True

    def tick(self):
        raw = self.stream.read(self.sampleinfo.chunk, exception_on_overflow=False)
        self.rawaudio = np.frombuffer(raw, dtype=np.float32)
    
    def process(self):
        # Silence detection
        if np.max(self.rawaudio) > self.silence_threshold:
            self.silent_frames = 0

            if not self.active:
                print("Audio active")
                self.active = True
        
        else:
            self.silent_frames += 1

            if self.active and self.silent_frames > (self.sampleinfo.fps * self.silence_seconds):
                print("Audio inactive")
                self.active = False
        
        self.audio_data = self.rawaudio if self.active else None
        self.audio_data_fft = abs(fft.rfft(self.rawaudio)) if self.active else None

    def is_active(self):
        return self.active

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()