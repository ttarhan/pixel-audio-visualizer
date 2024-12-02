import os
import time
import pyaudio
import numpy as np
from scipy import fftpack as fft
import sacn

from .config import AUDIO_ELEMENTS, FULLTIME_ELEMENTS, ELEMENTS, DMX_FPS, FORMAT, CHANNELS, RATE, CHUNK, SILENCE_THRESHOLD, SILENCE_SECONDS, FRAME_FPS

np.set_printoptions(threshold=500000)

BIND_ADDRESS = os.environ.get("BIND_ADDRESS", "0.0.0.0")

class Visualizer(object):
    """
    The audio analyzer
    """

    def __init__(self):
        self.sender = None
        self.audio_universes = tuple(universe for element in AUDIO_ELEMENTS for universe in element.get_universes())
        self.fulltime_universes = tuple(universe for element in FULLTIME_ELEMENTS for universe in element.get_universes())
        self.universes = [*self.audio_universes, *self.fulltime_universes]

    def _start_universes(self, universes):
        for universe in universes:
            self.sender.activate_output(universe)
            self.sender[universe].multicast = True

    def _stop_universes(self, universes):
        for universe in universes:
            self.sender.deactivate_output(universe)

    def run(self):
        """
        Starts listening for audio
        """
        # Startup
        self.sender = sacn.sACNsender(fps=DMX_FPS,
                                      universeDiscovery=False,
                                      bind_address=BIND_ADDRESS)
        
        self.sender.start()
        
        self._start_universes(self.fulltime_universes)
        
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        # Main loop
        lt = time.time()
        run = True
        audio_elements_active = False
        silent_frames = 0

        print("Running")

        while run:
            # Input
            raw = stream.read(CHUNK, exception_on_overflow=False)
            audio = np.frombuffer(raw, dtype=np.float32)
            
            # Silence detection
            if np.max(audio) > SILENCE_THRESHOLD:
                silent_frames = 0

                if not audio_elements_active:
                    print("Starting audio elements")
                    self._start_universes(self.audio_universes)
                    audio_elements_active = True
            
            else:
                silent_frames += 1

                if audio_elements_active and silent_frames > (FRAME_FPS * SILENCE_SECONDS):
                    print("Stopping audio elements")
                    self._stop_universes(self.audio_universes)
                    audio_elements_active = False

            # Get ready to process elements
            elements_to_process = [*FULLTIME_ELEMENTS]
            audiofft = None

            # Audio elements
            if audio_elements_active:
                # Analyze the spectrum
                audiofft = abs(fft.rfft(audio))
                elements_to_process.extend(AUDIO_ELEMENTS)
            
            # Process elements
            universe_data = dict()

            for e in elements_to_process:
                render_result = e.render(audio, audiofft)
                universe_data.update(render_result)

            # Process output
            for universe, current_universe_data in universe_data.items():
                flatened = np.reshape(current_universe_data, -1) # Flatten RGB
                flatened = tuple(flatened.tobytes())
                self.sender[universe].dmx_data = flatened

            # print(f'Diff: {round(time.time()-lt,4)}')
            lt = time.time()

        # Cleanup
        self.sender.stop()
        stream.stop_stream()
        stream.close()
        audio.terminate()