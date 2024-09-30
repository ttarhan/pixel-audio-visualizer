import os
import time
import pyaudio
import numpy as np
from scipy import fftpack as fft
import sacn
from config import *

np.set_printoptions(threshold=500000)

BIND_ADDRESS = os.environ.get("BIND_ADDRESS", "0.0.0.0")

class AudioAnalyer(object):
    """
    The audio analyzer
    """

    def __init__(self):
        self.sender = None

    def _start_sender(self):
        self._stop_sender()

        self.sender = sacn.sACNsender(fps=DMX_FPS, 
                                      universeDiscovery=False, 
                                      bind_address=BIND_ADDRESS)

        for (i,_count) in enumerate(UNIVERSE_LAYOUT):
            universe = i + UNIVERSE_START
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
            dmx = np.full((LEDS, 3), 0, dtype = np.uint8)

            for p in PROCESSORS:
                p.frame(audio, audiofft, dmx)

            # Process output
            chan = 0

            for (i,count) in enumerate(UNIVERSE_LAYOUT):
                universe = i + UNIVERSE_START
                endchan = chan + count - 1
                # print(f'U: {universe}, Chan: {chan}, End: {endchan}')
                # print(np.reshape(dmx[chan:endchan + 1], -1))

                array = np.reshape(dmx[chan:endchan + 1], -1) # Flatten RGB
                array = tuple(array.tobytes())
                self.sender[universe].dmx_data = array

                # print(sender[universe].dmx_data)
                chan += count

            # print(f'Diff: {round(time.time()-lt,4)}')
            lt = time.time()

        # Cleanup
        self._stop_sender()
        stream.stop_stream()
        stream.close()
        audio.terminate()

AudioAnalyer().run()
