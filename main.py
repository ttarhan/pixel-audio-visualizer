import pyaudio
import numpy as np
from scipy import fftpack as fft
import sacn
import time
from config import *

np.set_printoptions(threshold=500000)

class AudioAnalyer(object):

    def __init__(self):
        pass

    def run(self):
        # Startup
        sender = sacn.sACNsender(fps=DMX_FPS)

        for (i,count) in enumerate(UNIVERSE_LAYOUT):
            universe = i + UNIVERSE_START
            sender.activate_output(universe)
            sender[universe].multicast = True

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
                    sender.start()
                    active = True
            
            else:
                silent_frames += 1

                if active and silent_frames > (FRAME_FPS * SILENCE_SECONDS):
                    print("Stopping")
                    sender.stop()
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
                sender[universe].dmx_data = np.reshape(dmx[chan:endchan + 1], -1) # Flatten RGB
                # print(sender[universe].dmx_data)
                chan += count

            # print(f'Diff: {round(time.time()-lt,4)}')
            lt = time.time()

        # Cleanup
        sender.stop()
        stream.stop_stream()
        stream.close()
        audio.terminate()

AudioAnalyer().run()