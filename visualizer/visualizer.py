import os
import time
import pyaudio
import numpy as np
from scipy import fftpack as fft
import sacn

from .config import ELEMENTS, DMX_FPS, FORMAT, CHANNELS, RATE, CHUNK, SILENCE_THRESHOLD, SILENCE_SECONDS, FRAME_FPS

np.set_printoptions(threshold=500000)

BIND_ADDRESS = os.environ.get("BIND_ADDRESS", "0.0.0.0")

class Visualizer(object):
    """
    The audio analyzer
    """

    def __init__(self):
        self.sender = None
        self.universes = tuple(universe for element in ELEMENTS for universe in element.get_universes())

    def _start_sender(self):
        self._stop_sender()

        self.sender = sacn.sACNsender(fps=DMX_FPS,
                                      universeDiscovery=False,
                                      bind_address=BIND_ADDRESS)

        for universe in self.universes:
            self.sender.activate_output(universe)
            self.sender[universe].multicast = True

        self.sender.start()

    def _stop_sender(self):
        if self.sender:
            self.sender.stop()

        self.sender = None

    def run(self):
        """
        Starts listening for audio
        """
        # Startup
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        # Main loop
        lt = time.time()
        run = True
        active = False
        silent_frames = 0

        self._start_sender()
        active = True

        while run:
            # Input
            raw = stream.read(CHUNK, exception_on_overflow=False)
            audio = np.frombuffer(raw, dtype=np.float32)

            # Silence detection
            if np.max(audio) > SILENCE_THRESHOLD:
                silent_frames = 0

                if not active:
                    print("Starting")
                    self._start_sender()
                    active = True
            
            else:
                silent_frames += 1

                if active and silent_frames > (FRAME_FPS * SILENCE_SECONDS):
                    print("Stopping")
                    self._stop_sender()
                    active = False

            if not active:
                continue

            # Analyze the spectrum
            audiofft = abs(fft.rfft(audio))

            # Run processors
            universe_data = dict()

            for e in ELEMENTS:
                render_result = e.render(audio, audiofft)
                universe_data.update(render_result)

            # Process output
            for universe in self.universes:
                flatened = np.reshape(universe_data[universe], -1) # Flatten RGB
                flatened = tuple(flatened.tobytes())
                self.sender[universe].dmx_data = flatened

            # print(f'Diff: {round(time.time()-lt,4)}')
            lt = time.time()

        # Cleanup
        self._stop_sender()
        stream.stop_stream()
        stream.close()
        audio.terminate()