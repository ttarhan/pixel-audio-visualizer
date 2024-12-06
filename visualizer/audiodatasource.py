from typing import Optional
from dataclasses import dataclass

import pyaudio
import numpy as np
from numpy.typing import NDArray
from scipy import fftpack as fft

from .datasource import DataSource
from .clocksource import ClockSource


@dataclass
class SampleInfo:
    """
    Defines the audio sample parameters
    """

    rate: int
    chunk: int
    fps: int
    format: int
    channels: int


class AudioDataSource(DataSource, ClockSource):
    """
    A data source that reads audio data from a local audio input, and also
    serves as a clock source based on fixed-duration reads from the audio source.

    Must be used as the clock source to return audio frames.
    """

    def __init__(self, sampleinfo: SampleInfo, silence_threshold: float, silence_seconds: float):
        self.sampleinfo = sampleinfo
        self.silence_threshold = silence_threshold
        self.silence_seconds = silence_seconds

        self.pyaudio: Optional[pyaudio.PyAudio] = None
        self.stream: Optional[pyaudio.Stream] = None
        self.rawaudio: Optional[NDArray[np.float32]] = None
        self.silent_frames = 0
        self.active = False
        self.audio_data: Optional[NDArray[np.float32]] = None
        self.audio_data_fft: Optional[NDArray[np.float32]] = None
        self.running = False

    def start(self) -> None:
        if self.running:
            return

        self.pyaudio = pyaudio.PyAudio()

        self.stream = self.pyaudio.open(
            format=self.sampleinfo.format,
            channels=self.sampleinfo.channels,
            rate=self.sampleinfo.rate,
            input=True,
            frames_per_buffer=self.sampleinfo.chunk,
        )

        self.running = True

    def tick(self) -> None:
        if not self.active or self.stream is None:
            return

        raw = self.stream.read(self.sampleinfo.chunk, exception_on_overflow=False)
        self.rawaudio = np.frombuffer(raw, dtype=np.float32)

    def process(self) -> None:
        if self.rawaudio is None:
            return

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

    def is_active(self) -> bool:
        """
        Returns true if audio is currently being produced
        """
        return self.active

    def stop(self) -> None:
        """
        Shutdown the audio stream
        """
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        if self.pyaudio:
            self.pyaudio.terminate()
            self.pyaudio = None
